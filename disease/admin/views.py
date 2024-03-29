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
from disease.models import (
    Disease
)

# Serialier imports
from disease.admin.serializers import (
    DiseaseSerializer,
    DiseaseDetailsSerializer
)


# List Role
class DiseaseView(generics.ListCreateAPIView):
    model = Disease
    serializer_class = DiseaseSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = (
        'name',
        'code'
    )
    filter_fields = (
        'disease_category',
    )
    ordering_fields = (
        'name',
    )

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('name')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check code is existed
        disease = Disease.objects.filter(
            code=data.get('code')
        ).first()
        if disease:
            raise ValidationError(ErrorTemplate.DISEASE_CODE_ALREADY_EXISTED)

        serializer.save()

        return Response(serializer.data)


class DiseaseDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Disease
    serializer_class = DiseaseDetailsSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'disease_id'

    def get(self, request, *args, **kwargs):
        disease_id = self.kwargs.get(self.lookup_url_kwarg)
        disease = self.get_object(disease_id)

        # Get serializer
        serializer = self.serializer_class(instance=disease)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        disease_id = self.kwargs.get(self.lookup_url_kwarg)
        disease = self.get_object(disease_id)

        # Get serializer
        serializer = DiseaseSerializer(disease, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check code is existed
        disease_code_existed = Disease.objects.filter(
            code=data.get('code')
        ).exclude(
            id=disease.id
        ).first()
        if disease_code_existed:
            raise ValidationError(ErrorTemplate.DISEASE_CODE_ALREADY_EXISTED)

        disease = serializer.save()

        return Response(self.serializer_class(disease).data)

    def delete(self, request, *args, **kwargs):
        disease_id = self.kwargs.get(self.lookup_url_kwarg)
        disease = self.get_object(disease_id)

        disease.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        disease.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.DISEASE_NOT_EXIST)

        return obj