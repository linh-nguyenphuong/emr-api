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
    IsPhysician
)

# Model imports
from service.models import (
    Service
)

# Serialier imports
from service.user.serializers import (
    ServiceSerializer,
)

class ServiceView(generics.ListAPIView):
    model = Service
    serializer_class = ServiceSerializer
    permission_classes = (IsPhysician,)
    pagination_class = None
    search_fields = (
        'name',
    )
    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('name')

class ServiceDetailsView(generics.RetrieveAPIView):
    model = Service
    serializer_class = ServiceSerializer
    permission_classes = (IsPhysician,)
    lookup_url_kwarg = 'service_id'

    def get(self, request, *args, **kwargs):
        service_id = self.kwargs.get(self.lookup_url_kwarg)
        service = self.get_object(service_id)

        # Get serializer
        serializer = self.serializer_class(instance=service)

        return Response(serializer.data)
        
    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.SERVICE_NOT_EXIST)

        return obj