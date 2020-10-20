# Python imports
from datetime import datetime, timedelta
import jwt
import cloudinary.uploader

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
from user.profile.serializers import (
    PrivateProfileSerializer,
)

# Get - Update Profile
class ProfileDetailsView(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = PrivateProfileSerializer
    permission_classes = (IsUser,)

    def get(self, request, *args, **kwargs):
        user = self.get_object(request.user.id)
        
        # Get serializer
        serializer = self.serializer_class(instance=user)
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = self.get_object(request.user.id)
        
        # Get serializer
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        if data.get('phone') and not data.get('phone') == '':
            # Check phone existed
            phone = self.model.objects.filter(
                phone=data.get('phone'),
                is_deleted=False
            ).exclude(
                id=user.id
            ).first()
            if phone:
                return Response(ErrorTemplate.PHONE_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Check user role
                if user.role.name == 'patient':
                    return Response(ErrorTemplate.CANNOT_UPDATE_PHONE, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.phone = phone

        if data.get('email') and not data.get('email') == '':
            # Check email existed
            email = self.model.objects.filter(
                email=data.get('email'),
                is_deleted=False
            ).exclude(
                id=user.id
            ).first()
            if email:
                return Response(ErrorTemplate.EMAIL_ALREADY_EXISTED, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Check user role
                if not user.role.name == 'patient':
                    return Response(ErrorTemplate.CANNOT_UPDATE_EMAIL, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.email = email

        user.__dict__.update(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            DOB=data.get('DOB'),
            gender=data.get('gender')
        )
            
        # Save to database
        user.save()

        return Response(serializer.data)

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.USER_NOT_EXIST)

        return obj


# Upload User's avatar
class UploadUserAvatarView(generics.UpdateAPIView):
    model = User
    serializer_class = PrivateProfileSerializer
    permission_classes = (IsUser,)

    def patch(self, request, *args, **kwargs):
        profile = self.get_profile(request.user.id)
        
        # try:
        file = request.FILES.get('image')
        if not file:
            return Response(ErrorTemplate.IMAGE_REQUIRED, status.HTTP_400_BAD_REQUEST)

        uploaded_file = cloudinary.uploader.upload(
            file,
            folder='emr/user_avatar/', 
        )
        profile.__dict__.update(
            avatar=uploaded_file.get('secure_url')
        )

        # Save to database
        profile.save()

        serializer = self.serializer_class(instance=profile)

        return Response(serializer.data)
        # except:
        #     return Response(ErrorTemplate.UserError.CANNOT_UPLOAD_IMAGE, status.HTTP_417_EXPECTATION_FAILED)

    def get_profile(self, user_id):
        profile = self.model.objects.filter(
            id=user_id,
            is_deleted=False
        ).first()

        if not profile:
            raise ValidationError(ErrorTemplate.UserError.PROFILE_NOT_FOUND)

        return profile