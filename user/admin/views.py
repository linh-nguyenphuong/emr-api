# Python imports
from datetime import datetime, timedelta
import jwt

# Django imports
from django.core.mail import send_mail
from django.conf import settings
from django.utils import dateparse

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
    IsAdmin,
    IsUser
)
from templates.email_template import (
    EmailTemplate
)

# Model imports
from user.models import User
from role.models import Role

# Serialier imports
from user.admin.serializers import (
    UserSerializer,
)

class UserView(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    search_fields = (
        'first_name',
        'last_name',
        'email', 
        'phone'
    )

    def get_queryset(self):
        return self.model.objects.filter(
            is_deleted=False
        ).order_by('created_at')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        # Check phone existed
        if not data.get('phone') or data.get('phone') == '':
            return Response(ErrorTemplate.PHONE_REQUIRED, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone = self.model.objects.filter(
                phone=data.get('phone'),
            ).first()
            if phone:
                return Response(ErrorTemplate.PHONE_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)

        # Check role exist
        role = Role.objects.filter(
            id=data.get('role_id'),
        ).first()
        if not role:
            return Response(ErrorTemplate.ROLE_NOT_EXIST, status=status.HTTP_400_BAD_REQUEST)

        user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            phone= data.get('phone'),
            DOB=data.get('DOB'),
            role=role
        )
        user.set_password(data.get('password'))

        # Complete create account for Admin, Physcian, Receptionist
        if role.name in ('admin', 'receptionist', 'physician'):
            if not data.get('email') or data.get('email') == '':
                return Response(ErrorTemplate.EMAIL_REQUIRED, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Check email existed
                email = self.model.objects.filter(
                    email=data.get('email'),
                ).first()
                if email:
                    return Response(ErrorTemplate.EMAIL_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)
                user.email = data.get('email')
            
        # Save to database
        user.save()

        # Send activation link to user's email address
        url = 'http://127.0.0.1:8000/api/auth/verify-email'
        token = user.verify_email_token
        send_mail(
            subject=EmailTemplate.EmailConfirmation.SUBJECT,
            html_message=EmailTemplate.EmailConfirmation.BODY.format(user.first_name, '{0}/{1}/'.format(url, token)),
            message='',
            from_email=settings.FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        serializer = self.serializer_class(instance=user)
        return Response(serializer.data)

# Retrieve - Update - Delete User
class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_object(user_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=user)
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_object(user_id)
        
        # Get serializer
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        # Check phone existed
        if not data.get('phone') or data.get('phone') == '':
            return Response(ErrorTemplate.PHONE_REQUIRED, status=status.HTTP_400_BAD_REQUEST)
        else:
            phone = self.model.objects.filter(
                phone=data.get('phone'),
                is_deleted=False
            ).exclude(
                id=user.id
            ).first()
            if phone:
                return Response(ErrorTemplate.PHONE_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)

        # Check role exist
        role = Role.objects.filter(
            id=data.get('role_id'),
        ).first()
        if not role:
            return Response(ErrorTemplate.ROLE_NOT_EXIST, status=status.HTTP_400_BAD_REQUEST)    

        user.__dict__.update(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            phone= data.get('phone'),
            DOB=data.get('DOB'),
            role_id=role.id
        )

        # Complete create account for Admin, Physcian, Receptionist
        if role.name == 'patient':
            if not data.get('email') or data.get('email') == '':
                return Response(ErrorTemplate.EMAIL_REQUIRED, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Check email existed
                email = self.model.objects.filter(
                    email=data.get('email'),
                    is_deleted=False
                ).exclude(
                    id=user.id
                ).first()
                if email:
                    return Response(ErrorTemplate.EMAIL_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)
                user.email = data.get('email')
        else:
            if data.get('email') and not data.get('email') == '':
                return Response(ErrorTemplate.CANNOT_UPDATE_EMAIL, status=status.HTTP_400_BAD_REQUEST)
            
        # Save to database
        user.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_object(user_id)

        user.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        user.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.USER_NOT_EXIST)

        return obj

# Block User
class BlockUser(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_user(user_id)
        serializer = self.serializer_class(instance=user)

        # Check created account time
        if user.created_at > request.user.created_at:
            Response(ErrorTemplate.NOT_BLOCK_OLDER_ADMIN, status.HTTP_400_BAD_REQUEST)

        if user.is_active == True:
            user.__dict__.update(
                is_active=False,
                modified_by=request.user.id
            )
            user.save()

        return Response(serializer.data)

    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id
        ).first()

        if not user:
            raise ValidationError(ErrorTemplate.PROFILE_NOT_FOUND)

        return user

# Unblock User
class UnblockUser(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'user_id'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        user = self.get_user(user_id)
        serializer = self.serializer_class(instance=user)

        if user.is_active == False:
            user.__dict__.update(
                is_active=True,
                modified_by=request.user.id
            )
            user.save()

        return Response(serializer.data)

    def get_user(self, user_id):
        user = self.model.objects.filter(
            id=user_id
        ).first()

        if not user:
            raise ValidationError(ErrorTemplate.PROFILE_NOT_FOUND)

        return user