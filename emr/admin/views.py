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
            raise ValidationError(ErrorTemplate.PHYSICIAN_REQUIRED)

        emr = serializer.save(created_by=self.request.user,
                              total=total)

        data_drug = self.request.data.get('drug')
        if data_drug:
            for drug in data_drug:
                if Drug.objects.filter(id=drug['drug'], is_deleted=False).exists() and \
                        DrugInstruction.objects.filter(id=drug['drug_instruction']).exists():
                    EmrDrug.objects.create(emr=emr,
                                           drug=drug['drug'],
                                           drug_instruction=drug['drug_instruction'],
                                           quantity=drug['quantity'],
                                           unit_price=drug['unit_price'])
                    total = total + drug['quantity']
        data_disease = self.request.data.get('disease')
        if data_disease:
            for disease in data_disease:
                disease = Disease.objects.filter(id=disease).first()
                if disease:
                    EmrDisease.objects.create(emr=emr,
                                              disease=disease)

        data_service = self.request.data.get('service')
        if data_service:
            for service in data_disease:
                service = Service.objects.filter(id=service).first()
                if service:
                    PatientService.objects.create(emr=emr,
                                                  service=service,
                                                  created_at=datetime.now())

        data_image = self.request.data.get('image')
        if data_image:
            for image in data_image:
                EmrImage.objects.create(emr=emr,
                                        url=image)
        emr.total = total
        emr.save()
        return Response(serializer.data)
#
#
# class DrugDetailsView(generics.RetrieveUpdateDestroyAPIView):
#     model = Drug
#     serializer_class = DrugDetailsSerializer
#     permission_classes = (IsAdmin,)
#     lookup_url_kwarg = 'drug_id'
#
#     def get(self, request, *args, **kwargs):
#         drug_id = self.kwargs.get(self.lookup_url_kwarg)
#         drug = self.get_object(drug_id)
#
#         # Get serializer
#         serializer = self.serializer_class(instance=drug)
#
#         return Response(serializer.data)
#
#     def put(self, request, *args, **kwargs):
#         drug_id = self.kwargs.get(self.lookup_url_kwarg)
#         drug = self.get_object(drug_id)
#
#         # Get serializer
#         serializer = DrugSerializer(drug, data=request.data)
#         serializer.is_valid(raise_exception=False)
#         drug = serializer.save()
#
#         return Response(self.serializer_class(drug).data)
#
#     def delete(self, request, *args, **kwargs):
#         drug_id = self.kwargs.get(self.lookup_url_kwarg)
#         drug = self.get_object(drug_id)
#
#         drug.__dict__.update(
#             is_deleted=True,
#         )
#
#         # Save to database
#         drug.save()
#
#         return Response({
#             'message': 'Deleted successfully'
#         })
#
#     def get_object(self, object_id):
#         obj = self.model.objects.filter(
#             id=object_id,
#             is_deleted=False
#         ).first()
#
#         if not obj:
#             raise ValidationError(ErrorTemplate.DRUG_NOT_EXIST)
#
#         return obj