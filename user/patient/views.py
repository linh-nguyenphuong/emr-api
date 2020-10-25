# Python imports
from datetime import datetime, timedelta
import jwt

# Django imports
from django.core.mail import send_mail
from django.conf import settings
from django.utils import dateparse
from django.db.models import Q, Sum, Count
from django.utils import timezone


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
    IsUser,
    IsPhysicianOrReceptionist
)
from templates.email_template import (
    EmailTemplate
)

# Model imports
from user.models import User
from role.models import Role
from emr.models import Emr

# Serialier imports
from user.patient.serializers import (
    PatientSerializer,
)
from emr.user.serializers import EmrSerializer

# List - Create Patient
class PatientView(generics.ListCreateAPIView):
    model = User
    serializer_class = PatientSerializer
    permission_classes = (IsPhysicianOrReceptionist,)
    pagination_class = PageNumberPagination
    search_fields = (
        'first_name',
        'last_name',
        'phone'
    )
    filter_fields = {
        'role__name': ['exact'],
    }

    def get_queryset(self):
        return self.model.objects.filter(
            role__name='patient',
            is_deleted=False
        ).order_by('-created_at')

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

        user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            address=data.get('address'),
            phone= data.get('phone'),
            DOB=data.get('DOB'),
            gender=data.get('gender'),
            role_id=4
        )
        user.set_password(data.get('password'))

        # Save to database
        user.save()

        serializer = self.serializer_class(instance=user)
        return Response(serializer.data)

# Retrieve Patient
class PatientDetailsView(generics.RetrieveAPIView):
    model = User
    serializer_class = PatientSerializer
    permission_classes = (IsPhysicianOrReceptionist,)
    lookup_url_kwarg = 'patient_id'

    def get(self, request, *args, **kwargs):
        patient_id = self.kwargs.get(self.lookup_url_kwarg)
        patient = self.get_object(patient_id)

        if not patient.role.name == 'patient':
            raise ValidationError(ErrorTemplate.PATIENT_NOT_EXIST)

        # Get serializer
        serializer = self.serializer_class(instance=patient)
        
        return Response(serializer.data)

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.USER_NOT_EXIST)

        return obj
