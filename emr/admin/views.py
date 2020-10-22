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
from emr.models import (
    Emr,
    EmrImage
)
from emr_drug.models import EmrDrug
from emr_disease.models import EmrDisease
from patient_service.models import PatientService
from drug.models import Drug
from drug_instruction.models import DrugInstruction
from disease.models import Disease
from service.models import Service

from user.models import User

# Serialier imports
from emr.admin.serializers import (
    EmrSerializer,
    EmrImageSerializer
)


# List Role
class EmrView(generics.ListCreateAPIView):
    model = Emr
    serializer_class = EmrSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = (
        'patient__first_name',
        'patient__last_name'
    )
    filter_fields = (
        'created_at',
        'status'
    )

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        total = 0
        patient = data['patient']
        if not patient or not patient.role.name == 'patient':
            raise ValidationError(ErrorTemplate.PATIENT_REQUIRED)

        patient = data['physician']
        if not patient or not patient.role.name == 'physician':
            raise ValidationError(ErrorTemplate.PHYSICIAN_NOT_EXIST)

        data['status'] = 'pending'
        serializer.save(created_by=self.request.user,
                        total=total)
        return Response(serializer.data)


class EmrDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Emr
    serializer_class = EmrSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'emr_id'

    def get(self, request, *args, **kwargs):
        emr_id = self.kwargs.get(self.lookup_url_kwarg)
        emr = self.get_object(emr_id)

        # Get serializer
        serializer = self.serializer_class(instance=emr)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        emr_id = self.kwargs.get(self.lookup_url_kwarg)
        emr = self.get_object(emr_id)

        # Get serializer
        serializer = EmrSerializer(emr, data=request.data)
        serializer.is_valid(raise_exception=False)
        drug = serializer.save()

        return Response(self.serializer_class(drug).data)

    def delete(self, request, *args, **kwargs):
        emr_id = self.kwargs.get(self.lookup_url_kwarg)
        emr = self.get_object(emr_id)

        emr.__dict__.update(
            is_deleted=True,
        )

        EmrImage.objects.filter(emr=emr).update(is_deleted=True)
        EmrDrug.objects.filter(emr=emr).update(is_deleted=True)
        EmrDisease.objects.filter(emr=emr).update(is_deleted=True)
        PatientService.objects.filter(emr=emr).update(is_deleted=True)
        # Save to database
        emr.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        return obj


class EmrImageAddView(generics.CreateAPIView):
    model = EmrImage
    serializer_class = EmrImageSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'emr_id'

    def post(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(emr=emr)

        return Response(serializer.data)


class EmrImageRemoveView(generics.DestroyAPIView):
    model = EmrImage
    permission_classes = (IsAdmin,)
    pagination_class = None
    lookup_url_kwarg = 'emr_image_id'

    def delete(self, request, *args, **kwargs):

        emr_image = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()

        emr_image.__dict__.update(
            is_deleted=True,
        )
        emr_image.save()

        return Response({
            'message': 'Deleted successfully'
        })


class EmrCompleteView(generics.ListAPIView):
    model = EmrImage
    serializer_class = EmrSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'emr_id'

    def get(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        emr.status = 'complete'
        emr.save()

        return Response(self.serializer_class(emr).data)


class EmrPaidView(generics.ListAPIView):
    model = EmrImage
    serializer_class = EmrSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'emr_id'

    def get(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        emr.is_paid = True
        emr.save()

        return Response(self.serializer_class(emr).data)
