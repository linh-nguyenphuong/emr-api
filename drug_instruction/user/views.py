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
from drug_instruction.models import (
    DrugInstruction
)

# Serialier imports
from drug_instruction.user.serializers import (
    DrugInstructionSerializer,
)

class DrugInstructionView(generics.ListAPIView):
    model = DrugInstruction
    serializer_class = DrugInstructionSerializer
    permission_classes = (IsPhysician,)
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('instruction')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class DrugInstructionDetailsView(generics.RetrieveAPIView):
    model = DrugInstruction
    serializer_class = DrugInstructionSerializer
    permission_classes = (IsPhysician,)
    lookup_url_kwarg = 'drug_instruction_id'

    def get(self, request, *args, **kwargs):
        drug_instruction_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_instruction = self.get_object(drug_instruction_id)

        # Get serializer
        serializer = self.serializer_class(instance=drug_instruction)

        return Response(serializer.data)

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.DRUG_INSTRUCTION_NOT_EXIST)

        return obj