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
from emr.models import Emr
from emr_disease.models import EmrDisease

# Serialier imports
from emr_disease.admin.serializers import (
    EmrDiseaseSerializer,
)


# List Role
class EmrDiseaseAddView(generics.CreateAPIView):
    model = EmrDisease
    serializer_class = EmrDiseaseSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None
    lookup_url_kwarg = 'emr_id'

    def post(self, request, *args, **kwargs):
        emr = Emr.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()
        if not emr:
            raise ValidationError(ErrorTemplate.EMR_NOT_EXIST)

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        EmrDisease.objects.create(emr=emr,
                                  disease=data['disease'])
        return Response(serializer.data)


class EmrDiseaseRemoveView(generics.DestroyAPIView):
    model = EmrDisease
    permission_classes = (IsAdmin,)
    pagination_class = None
    lookup_url_kwarg = 'emr_disease_id'

    def delete(self, request, *args, **kwargs):

        emr_disease = self.model.objects.filter(id=self.kwargs.get(self.lookup_url_kwarg)).first()

        emr_disease.__dict__.update(
            is_deleted=True,
        )
        emr_disease.save()

        return Response({
            'message': 'Deleted successfully'
        })


