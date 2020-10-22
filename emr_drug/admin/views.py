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
from emr_drug.models import (
    EmrDrug
)
from emr.models import Emr
from drug_instruction.models import DrugInstruction

# Serialier imports
from emr_drug.admin.serializers import (
    EmrDrugSerializer,
)


# List Role
class EmrDrugAddView(generics.CreateAPIView):
    model = EmrDrug
    serializer_class = EmrDrugSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None
    lookup_url_kwarg = 'emr_id'

    def post(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        total = 0

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data['drug_instruction']:
            serializer.save(emr=emr)

            drug_emr = self.model.objects.filter(emr=emr, is_deleted=False)
            for drug in drug_emr:
                total = total + drug.quantity
                emr.total = total
                emr.save()

            return Response(serializer.data)

        raise ValidationError(ErrorTemplate.DRUG_INSTRUCTION_NOT_EXIST)


class EmrDrugRemoveView(generics.DestroyAPIView):
    model = EmrDrug
    permission_classes = (IsAdmin,)
    pagination_class = None
    lookup_url_kwarg = 'emr_drug_id'

    def delete(self, request, *args, **kwargs):

        emr_drug = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()

        emr_drug.__dict__.update(
            is_deleted=True,
        )
        emr_drug.save()

        total = 0
        emr = Emr.objects.filter(id=self.kwargs.get('emr_id')).first()
        drug_emr = self.model.objects.filter(emr=emr, is_deleted=False)
        for drug in drug_emr:
            total = total + drug.quantity
            emr.total = total
            emr.save()

        return Response({
            'message': 'Deleted successfully'
        })


