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
from patient_service.models import PatientService
from service.models import Service
from emr.models import Emr

# Serialier imports
from patient_service.admin.serializers import (
    EmrServiceSerializer,
)
from service.admin.serializers import ServiceSerializer


# List Role
class EmrServiceView(generics.ListCreateAPIView):
    model = PatientService
    serializer_class = EmrServiceSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None
    lookup_url_kwarg = 'emr_id'

    def get_queryset(self):
        self.serializer_class = ServiceSerializer
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        list_service = PatientService.objects.filter(emr=emr, is_deleted=False)
        return Service.objects.filter(id__in=(list_service.values_list('service', flat=True)))

    def post(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(emr=emr)

        return Response(serializer.data)


class EmrServiceRemoveView(generics.DestroyAPIView):
    model = PatientService
    permission_classes = (IsAdmin,)
    pagination_class = None
    lookup_url_kwarg = 'emr_service_id'

    def delete(self, request, *args, **kwargs):

        emr_service = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()

        emr_service.__dict__.update(
            is_deleted=True,
        )
        emr_service.save()

        return Response({
            'message': 'Deleted successfully'
        })


