# Python imports
from datetime import datetime, timedelta
import jwt

# Django imports
from django.core.mail import send_mail
from django.conf import settings
from django.utils import dateparse
from django.db.models import Q
from django.contrib.auth import get_user_model

# Django REST framework imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import (
    APIView,
)
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed
)
from rest_framework.pagination import PageNumberPagination

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsUser
)
from templates.email_template import (
    EmailTemplate
)

# Model imports
from user.models import User

# Serialier imports
from user.auth.serializers import (
    VerifyEmailSerializer,
    LoginSerializer,
    ChangePasswordSerializer
)

class VerifyEmailView(APIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = ()
    lookup_url_kwarg = 'token'

    def get(self, request, *args, **kwargs):
        token = self.kwargs.get(self.lookup_url_kwarg)
        try:
            token_data = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise AuthenticationFailed(msg)
        
        # Check token type
        if not token_data.get('token_type') == 'verify_email':
            msg = 'The token must be activation account token.'
            raise AuthenticationFailed(msg)

        # Check user exist
        user = User.objects.filter(
            pk=token_data.get('user_id')
        ).first()
        if not user:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        
        # Check token expired
        if datetime.now() > datetime.strptime(token_data.get('expired_at'), '%c'):
            msg = 'The token has expired.'
            raise AuthenticationFailed(msg)

        serializer = self.serializer_class(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check user has verified their account
        if user.is_verified_email:
            raise ValidationError(ErrorTemplate.VERIFIED_EMAIL)

        # Check account created date is valid
        if user.created_at + timedelta(days=7) < datetime.now():
            raise ValidationError(ErrorTemplate.EXPIRED_LINK)

        # Change is_verified_email status
        user.is_verified_email = True

        # Save to database
        user.save()

        return Response(serializer.data)

class LoginView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        email = ''
        phone = ''
        if data.get('email'):
            email = data.get('email')
        if data.get('phone'):
            phone = data.get('phone')
        password = data.get('password')

        # Fetch the user by searching the email or phone
        user = User.objects.filter(
            Q(email=email) | Q(phone=phone)
        ).first()
        if not user:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
            raise ValidationError(ErrorTemplate.INCORRECT_EMAIL_OR_PHONE)

        # Check email is verified
        if not email == '' and not user.is_verified_email:
            raise ValidationError(ErrorTemplate.VERIFIED_EMAIL_REQUIRED)

        # Check phone is verified
        if not phone == '' and not user.is_verified_phone:
            raise ValidationError(ErrorTemplate.VERIFIED_PHONE_REQUIRED)

        # Check password
        password_correct = user.check_password(password)
        if not password_correct:
            raise ValidationError(ErrorTemplate.INCORRECT_PASSWORD)
        
        return Response({
            'access_token': user.access_token,
            'refresh_token': user.refresh_token
        })
    

class RefreshTokenView(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        token = self.request.data.get('refresh_token')

        try:
            token_data = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise AuthenticationFailed(msg)
        
        # Check token type
        if not token_data.get('token_type') == 'refresh':
            msg = 'The token must be refresh token.'
            raise AuthenticationFailed(msg)

        # Check user exist
        user = User.objects.filter(
            pk=token_data.get('user_id')
        ).first()
        if not user:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        
        # Check token expired
        if datetime.now() > datetime.strptime(token_data.get('expired_at'), '%c'):
            msg = 'The token has expired.'
            raise AuthenticationFailed(msg)

        return Response({
            'access_token': user.access_token
        })

class ChangePasswordView(generics.UpdateAPIView):
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsUser,)

    def put(self, request, *args, **kwargs):
        user = self.get_user(request.user.id)
        serializer = self.serializer_class(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # Check password
        password_correct = user.check_password(data.get('old_password'))
        if not password_correct:
            raise ValidationError(ErrorTemplate.INCORRECT_PASSWORD)

        # Check password and repeat password matched
        if not data.get('new_password') == data.get('confirm_password'):
            raise ValidationError(ErrorTemplate.PASSWORDS_NOT_MATCH)

        user.set_password(data.get('new_password'))

        # Save to database
        user.save()

        return Response({
            'message': 'Password successfully updated.',
        })
    
    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id,
        ).first()
        if not user:
            return Response(ErrorTemplate.USER_NOT_EXISTED)
        
        return user

# Send reset password link to user        
class ForgotPasswordView(APIView):
    model = User
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = self.request.data

        # Check email exist
        user = self.model.objects.filter(
            email=data.get('email')
        ).first()
        if not user:
            return Response(ErrorTemplate.EMAIL_NOT_EXISTED, status.HTTP_400_BAD_REQUEST)
        
        # Send validation link to user's email address
        url = 'http://127.0.0.1:8000/api/auth/forgot-password'
        token = user.verify_reset_password_token
        send_mail(
            subject=EmailTemplate.ForgotPasswordConfirmation.SUBJECT,
            html_message=EmailTemplate.ForgotPasswordConfirmation.BODY.format(user.first_name, '{0}/{1}/'.format(url, token)),
            message='',
            from_email=settings.FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        return Response({
            'message': 'Password reset link has been sent to your email.',
        })

# Verify reset password link, create new password
class ForgotPasswordDetailsView(APIView):
    model = User
    permission_classes = ()
    lookup_url_kwarg = 'token'

    def get(self, request, *args, **kwargs):
        token = self.kwargs.get(self.lookup_url_kwarg)
        
        user = self.verify_forgot_password_token(token)
        if not user:
            return Response(ErrorTemplate.INVALID_RESET_PASSWORD_LINK)

        return Response({
            'message': 'The token is valid.'
        })

    def post(self, request, *args, **kwargs):
        token = self.kwargs.get(self.lookup_url_kwarg)
        
        user = self.verify_forgot_password_token(token)
        if not user:
            return Response(ErrorTemplate.INVALID_RESET_PASSWORD_LINK)

        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response(ErrorTemplate.FIELDS_REQUIRED, status.HTTP_400_BAD_REQUEST)

        # Check password and repeat password matched
        if not new_password == confirm_password:
            raise ValidationError(ErrorTemplate.PASSWORDS_NOT_MATCH)

        user.set_password(new_password)

        # Update last reset password
        user.last_reset_password_at = datetime.now()

        # Save to database
        user.save()

        return Response({
            'message': 'Password reset successfully.'
        })

    def verify_forgot_password_token(self, token):
        try:
            token_data = jwt.decode(token, settings.SECRET_KEY)
        except:
            return None
        
        # Check token type
        if not token_data.get('token_type') == 'verify_reset_password':
            return None

        # Check user exist
        user = User.objects.filter(
            pk=token_data.get('user_id')
        ).first()
        if not user:
            return None
        
        # Check link has been expired
        if datetime.now() > dateparse.parse_datetime(token_data.get('expired_at')):
            return None

        # Check user already reset password
        if user.last_reset_password_at:
            if dateparse.parse_datetime(token_data.get('created_at')) < user.last_reset_password_at:
                return None
        return user