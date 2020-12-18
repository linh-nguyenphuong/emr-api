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

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsAdmin,
)

# Model imports
from service.models import (
    Service
)

# Serialier imports
from service.admin.serializers import (
    ServiceSerializer,
)


# List Role
class ServiceView(generics.ListCreateAPIView):
    model = Service
    serializer_class = ServiceSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None
    search_fields = (
        'name',
    )
    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('name')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check service is existed
        service = Service.objects.filter(
            name=data.get('name'),
            is_deleted=False
        ).first()
        if service:
            raise ValidationError(ErrorTemplate.SERVICE_ALREADY_EXISTED)

        serializer.save()

        return Response(serializer.data)


class ServiceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Service
    serializer_class = ServiceSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'service_id'

    def get(self, request, *args, **kwargs):
        service_id = self.kwargs.get(self.lookup_url_kwarg)
        service = self.get_object(service_id)

        # Get serializer
        serializer = self.serializer_class(instance=service)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        service_id = self.kwargs.get(self.lookup_url_kwarg)
        service = self.get_object(service_id)

        # Get serializer
        serializer = self.serializer_class(service, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        # Check service is existed
        service_name_existed = Service.objects.filter(
            name=data.get('name'),
            is_deleted=False
        ).exclude(
            id=service.id
        ).first()
        if service_name_existed:
            raise ValidationError(ErrorTemplate.SERVICE_ALREADY_EXISTED)

        service.__dict__.update(
            name=data.get('name'),
            price=data.get('price')
        )

        # Save to database
        service.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        drug_category_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_category = self.get_object(drug_category_id)

        drug_category.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        drug_category.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.SERVICE_NOT_EXIST)

        return obj