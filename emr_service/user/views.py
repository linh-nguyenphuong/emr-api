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
from emr_service.models import EmrService
from service.models import Service
from emr.models import Emr

# Serialier imports
from emr_service.user.serializers import (
    EmrServiceSerializer,
)
from service.user.serializers import ServiceSerializer

class EmrServiceView(generics.ListCreateAPIView):
    model = EmrService
    serializer_class = EmrServiceSerializer
    permission_classes = (IsAdminOrPhysician,)
    pagination_class = None
    lookup_url_kwarg = 'emr_id'

    def get_queryset(self):
        self.serializer_class = ServiceSerializer
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)
        list_service = EmrService.objects.filter(emr=emr, is_deleted=False)
        return Service.objects.filter(id__in=(list_service.values_list('service', flat=True)))

    def post(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        if emr.status == 'completed':
            raise ValidationError(ErrorTemplate.EMR_NOT_UPDATE)

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check service is valid
        service = Service.objects.filter(
            id=data.get('service_id'),
            is_deleted=False,
        ).first()
        if not service:
            raise ValidationError(ErrorTemplate.SERVICE_NOT_EXIST)

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        # Check service existed in the emr
        emr_service = EmrService.objects.filter(
            emr=emr,
            service=service,
            is_deleted=False
        ).first()
        if emr_service:
            raise ValidationError(ErrorTemplate.SERVICE_EXISTED_IN_EMR)

        serializer.save(emr=emr)

        # Update emr total
        emr.total = emr.total + service.price
        emr.save()

        return Response(serializer.data)

class EmrServiceRemoveView(generics.DestroyAPIView):
    model = EmrService
    permission_classes = (IsAdminOrPhysician,)
    pagination_class = None
    lookup_url_kwarg = 'emr_service_id'

    def delete(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get('emr_id')).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)
            
        if emr.status == 'completed':
            raise ValidationError(ErrorTemplate.EMR_NOT_UPDATE)

        emr_service = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr_service:
            raise ValidationError(ErrorTemplate.SERVICE_NOT_EXIST_IN_EMR)

        emr_service.__dict__.update(
            is_deleted=True,
        )
        emr_service.save()

        return Response({
            'message': 'Deleted successfully'
        })


