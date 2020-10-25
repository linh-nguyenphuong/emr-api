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
    IsPhysician,
    IsAdminOrPhysician
)

# Model imports
from emr_drug.models import (
    EmrDrug
)
from emr.models import Emr
from drug_instruction.models import DrugInstruction
from drug.models import Drug

# Serialier imports
from emr_drug.user.serializers import (
    EmrDrugSerializer,
)

class EmrDrugAddView(generics.CreateAPIView):
    model = EmrDrug
    serializer_class = EmrDrugSerializer
    permission_classes = (IsAdminOrPhysician,)
    pagination_class = None
    lookup_url_kwarg = 'emr_id'

    def post(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        if emr.status == 'completed':
            raise ValidationError(ErrorTemplate.EMR_NOT_UPDATE)

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check drug is valid
        drug = Drug.objects.filter(
            id=data.get('drug_id'),
            is_deleted=False,
        ).first()
        if not drug:
            raise ValidationError(ErrorTemplate.DRUG_NOT_EXIST)

        # Check drug existed in the emr
        emr_drug = EmrDrug.objects.filter(
            emr=emr,
            drug=drug,
            is_deleted=False
        ).first()
        if emr_drug:
            raise ValidationError(ErrorTemplate.DRUG_EXISTED_IN_EMR)
        
        # Check drug instruction exist
        drug_instruction = DrugInstruction.objects.filter(
            id=data.get('drug_instruction_id'),
            is_deleted=False
        ).first()
        if not drug_instruction:
            raise ValidationError(ErrorTemplate.DRUG_INSTRUCTION_NOT_EXIST)

        serializer.save(emr=emr)

        # Update emr total
        emr.total = emr.total + data.get('quantity') * drug.price
        emr.save()

        return Response(serializer.data)

class EmrDrugDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = EmrDrug
    serializer_class = EmrDrugSerializer
    permission_classes = (IsAdminOrPhysician,)
    pagination_class = None
    lookup_url_kwarg = 'emr_drug_id'

    def put(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get('emr_id')).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        if emr.status == 'completed':
            raise ValidationError(ErrorTemplate.EMR_NOT_UPDATE)

        emr_drug = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr_drug:
            raise ValidationError(ErrorTemplate.DRUG_NOT_EXIST_IN_EMR)

        serializer = self.serializer_class(instance=emr_drug, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = serializer.validated_data

        # Check drug is valid
        drug = Drug.objects.filter(
            id=data.get('drug_id'),
            is_deleted=False,
        ).first()
        if not drug:
            raise ValidationError(ErrorTemplate.DRUG_NOT_EXIST)

        # Check drug existed in the emr
        drug_in_emr = EmrDrug.objects.filter(
            emr=emr,
            drug=drug,
            is_deleted=False
        ).exclude(
            id=emr_drug.id
        ).first()
        if drug_in_emr:
            raise ValidationError(ErrorTemplate.DRUG_EXISTED_IN_EMR)

        # Check drug instruction exist
        drug_instruction = DrugInstruction.objects.filter(
            id=data.get('drug_instruction_id'),
            is_deleted=False
        ).first()
        if not drug_instruction:
            raise ValidationError(ErrorTemplate.DRUG_INSTRUCTION_NOT_EXIST)

        serializer.save()

        # Update emr total
        greater_or_less_quantity = data.get('quantity') - emr_drug.quantity
        emr.total = emr.total + greater_or_less_quantity * drug.price
            
        emr.save()

        return Response(serializer.data)


    def delete(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get('emr_id')).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        if emr.status == 'completed':
            raise ValidationError(ErrorTemplate.EMR_NOT_UPDATE)

        emr_drug = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr_drug:
            raise ValidationError(ErrorTemplate.DRUG_NOT_EXIST_IN_EMR)

        emr_drug.__dict__.update(
            is_deleted=True,
        )
        emr_drug.save()

        # Update emr total
        emr.total = emr.total - emr_drug.quantity * emr_drug.drug.price
        emr.save()

        return Response({
            'message': 'Deleted successfully'
        })


