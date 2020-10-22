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
from drug.models import (
    Drug
)

# Serialier imports
from drug.admin.serializers import (
    DrugSerializer,
    DrugDetailsSerializer
)


# List Role
class DrugView(generics.ListCreateAPIView):
    model = Drug
    serializer_class = DrugSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = (
        'name',
        'code'
    )
    filter_fields = (
        'drug_category',
    )
    ordering_fields = (
        'name',
    )

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('name')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class DrugDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Drug
    serializer_class = DrugDetailsSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'drug_id'

    def get(self, request, *args, **kwargs):
        drug_id = self.kwargs.get(self.lookup_url_kwarg)
        drug = self.get_object(drug_id)

        # Get serializer
        serializer = self.serializer_class(instance=drug)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        drug_id = self.kwargs.get(self.lookup_url_kwarg)
        drug = self.get_object(drug_id)

        # Get serializer
        serializer = DrugSerializer(drug, data=request.data)
        serializer.is_valid(raise_exception=False)
        drug = serializer.save()

        return Response(self.serializer_class(drug).data)

    def delete(self, request, *args, **kwargs):
        drug_id = self.kwargs.get(self.lookup_url_kwarg)
        drug = self.get_object(drug_id)

        drug.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        drug.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.DRUG_NOT_EXIST)

        return obj