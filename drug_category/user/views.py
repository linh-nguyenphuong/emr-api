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
from drug_category.models import (
    DrugCategory
)

# Serialier imports
from drug_category.user.serializers import (
    DrugCategorySerializer,
)

class DrugCategoryView(generics.ListAPIView):
    model = DrugCategory
    serializer_class = DrugCategorySerializer
    permission_classes = (IsPhysician,)
    pagination_class = None
    search_fields = (
        'name',
    )
    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('name')

class DrugCategoryDetailsView(generics.RetrieveAPIView):
    model = DrugCategory
    serializer_class = DrugCategorySerializer
    permission_classes = (IsPhysician,)
    lookup_url_kwarg = 'drug_category_id'

    def get(self, request, *args, **kwargs):
        drug_category_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_category = self.get_object(drug_category_id)

        # Get serializer
        serializer = self.serializer_class(instance=drug_category)

        return Response(serializer.data)

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.DRUG_CATEGORY_NOT_EXIST)

        return obj