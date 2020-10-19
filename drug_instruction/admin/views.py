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
from drug_instruction.models import (
    DrugInstruction
)

# Serialier imports
from drug_instruction.admin.serializers import (
    DrugInstructionSerializer,
)


# List Role
class DrugInstructionView(generics.ListCreateAPIView):
    model = DrugInstruction
    serializer_class = DrugInstructionSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('instruction')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class DrugInstructionDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = DrugInstruction
    serializer_class = DrugInstructionSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'drug_instruction_id'

    def get(self, request, *args, **kwargs):
        drug_instruction_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_instruction = self.get_object(drug_instruction_id)

        # Get serializer
        serializer = self.serializer_class(instance=drug_instruction)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        drug_instruction_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_instruction = self.get_object(drug_instruction_id)

        # Get serializer
        serializer = self.serializer_class(drug_instruction, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        drug_instruction.__dict__.update(
            instruction=data.get('instruction'),
        )

        # Save to database
        drug_instruction.save()

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
            raise ValidationError(ErrorTemplate.DRUG_CATEGORY_NOT_EXIST)

        return obj