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
    IsAdminOrPhysician
)

# Model imports
from emr.models import Emr
from emr_disease.models import EmrDisease
from disease.models import Disease

# Serialier imports
from emr_disease.user.serializers import (
    EmrDiseaseSerializer,
)

class EmrDiseaseAddView(generics.CreateAPIView):
    model = EmrDisease
    serializer_class = EmrDiseaseSerializer
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

        # Check disease exist
        disease = Disease.objects.filter(
            id=data.get('disease_id'),
            is_deleted=False,
        ).first()
        if not disease:
            raise ValidationError(ErrorTemplate.DISEASE_NOT_EXIST)

        # Check disease existed in the emr
        disease = EmrDisease.objects.filter(
            emr=emr, 
            disease_id=data.get('disease_id')
        ).first()
        if disease:
            raise ValidationError(ErrorTemplate.DISEASE_EXISTED_IN_EMR)

        serializer.save(
            emr_id=emr.id
        )

        return Response(serializer.data)

class EmrDiseaseRemoveView(generics.DestroyAPIView):
    model = EmrDisease
    permission_classes = (IsAdminOrPhysician,)
    pagination_class = None
    lookup_url_kwarg = 'emr_disease_id'

    def delete(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get('emr_id')).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        if emr.status == 'completed':
            raise ValidationError(ErrorTemplate.EMR_NOT_UPDATE)

        emr_disease = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr_disease:
            raise ValidationError(ErrorTemplate.DISEASE_NOT_EXIST_IN_EMR)

        emr_disease.__dict__.update(
            is_deleted=True,
        )
        emr_disease.save()

        return Response({
            'message': 'Deleted successfully'
        })


