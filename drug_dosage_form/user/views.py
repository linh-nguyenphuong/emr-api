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
    IsAdminOrPhysician
)

# Model imports
from drug_dosage_form.models import (
    DrugDosageForm
)

# Serialier imports
from drug_dosage_form.user.serializers import (
    DrugDosageFormSerializer,
)

class DrugDosageFormView(generics.ListAPIView):
    model = DrugDosageForm
    serializer_class = DrugDosageFormSerializer
    permission_classes = (IsAdminOrPhysician,)
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('name')

class DrugDosageFormDetailsView(generics.RetrieveAPIView):
    model = DrugDosageForm
    serializer_class = DrugDosageFormSerializer
    permission_classes = (IsAdminOrPhysician,)
    lookup_url_kwarg = 'drug_dosage_form_id'

    def get(self, request, *args, **kwargs):
        drug_dosage_form_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_dosage_form = self.get_object(drug_dosage_form_id)

        # Get serializer
        serializer = self.serializer_class(instance=drug_dosage_form)

        return Response(serializer.data)

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.DRUG_DOSAGE_FORM_NOT_EXIST)

        return obj