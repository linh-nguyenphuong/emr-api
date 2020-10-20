# Django imports
from django.utils import timezone
from datetime import datetime, timedelta
from pyfcm import FCMNotification
from django.conf import settings

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
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import (
    DjangoFilterBackend,
)

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsAdmin,
)

# Model imports
from appointment.models import (
    Appointment
)
from user.models import User
from role.models import Role

# Serialier imports
from appointment.admin.serializers import (
    AppointmentSerializer,

)


# List Role
class AppointmentView(generics.ListCreateAPIView):
    model = Appointment
    serializer_class = AppointmentSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('appointment_at')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        patient = data['patient']
        if not patient or not patient.role.name == 'patient':
            raise ValidationError(ErrorTemplate.PATIENT_REQUIRED)

        physician = data['physician']
        if not physician or not physician.role.name == 'physician':
            raise ValidationError(ErrorTemplate.PHYSICIAN_REQUIRED)

        data['created_by'] = self.request.user
        serializer.save()

        return Response(serializer.data)


class AppointmentDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Appointment
    serializer_class = AppointmentSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'appointment_id'

    def get(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get(self.lookup_url_kwarg)
        appointment = self.get_object(appointment_id)

        # Get serializer
        serializer = self.serializer_class(instance=appointment)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get(self.lookup_url_kwarg)
        appointment = self.get_object(appointment_id)
        if not appointment.status == 'accept':
        # Get serializer
            serializer = AppointmentSerializer(appointment, data=request.data)
            serializer.is_valid(raise_exception=False)
            data = serializer.validated_data

            patient = data['patient']
            if not patient or not patient.role.name == 'patient':
                raise ValidationError(ErrorTemplate.PATIENT_REQUIRED)

            physician = data['physician']
            if not physician or not physician.role.name == 'physician':
                raise ValidationError(ErrorTemplate.PHYSICIAN_REQUIRED)

            appointment = serializer.save()

            return Response(self.serializer_class(appointment).data)
        raise ValidationError(ErrorTemplate.APPOINTMENT_NOT_UPDATE)


    def delete(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get(self.lookup_url_kwarg)
        appointment = self.get_object(appointment_id)

        appointment.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        appointment.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.APPOINTMENT_NOT_EXIST)

        return obj


class AppointmentAcceptView(generics.UpdateAPIView):
    model = Appointment
    serializer_class = AppointmentSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'appointment_id'

    def put(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get(self.lookup_url_kwarg)
        appointment = self.get_object(appointment_id)
        # Get serializer
        appointment.status = 'accept'
        appointment.save()

        return Response(self.serializer_class(appointment).data)


    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.APPOINTMENT_NOT_EXIST)

        return obj


class AppointmentRejectView(generics.UpdateAPIView):
    model = Appointment
    serializer_class = AppointmentSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'appointment_id'

    def put(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get(self.lookup_url_kwarg)
        appointment = self.get_object(appointment_id)
        # Get serializer
        appointment.status = 'reject'
        appointment.save()

        return Response(self.serializer_class(appointment).data)


    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.APPOINTMENT_NOT_EXIST)

        return obj
