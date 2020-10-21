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
from visit.models import (
    Visit
)

# Serialier imports
from visit.admin.serializers import (
    VisitSerializer,
)


# List Role
class VisitView(generics.ListCreateAPIView):
    model = Visit
    serializer_class = VisitSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = (
        'visit_number',
        'patient__first_name',
        'patient__last_name'
    )
    filter_fields = (
        'created_at',
        'room',
    )

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('visit_number')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        patient = data['patient']
        if patient and patient.role.name == 'patient':
            serializer.save(created_by=self.request.user)
            return Response(serializer.data)
        raise ValidationError(ErrorTemplate.PATIENT_REQUIRED)



class VisitDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Visit
    serializer_class = VisitSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'visit_id'

    def get(self, request, *args, **kwargs):
        visit_id = self.kwargs.get(self.lookup_url_kwarg)
        visit = self.get_object(visit_id)

        # Get serializer
        serializer = self.serializer_class(instance=visit)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        visit_id = self.kwargs.get(self.lookup_url_kwarg)
        visit = self.get_object(visit_id)

        # Get serializer
        serializer = VisitSerializer(visit, data=request.data)
        serializer.is_valid(raise_exception=False)

        data = serializer.validated_data

        patient = data['patient']
        if patient and patient.role.name == 'patient':
            visit = serializer.save()
            return Response(self.serializer_class(visit).data)
        raise ValidationError(ErrorTemplate.PATIENT_REQUIRED)

    def delete(self, request, *args, **kwargs):
        visit_id = self.kwargs.get(self.lookup_url_kwarg)
        visit = self.get_object(visit_id)

        visit.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        visit.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.VISIT_NOT_EXIST)

        return obj


class PrintView(generics.ListCreateAPIView):
    model = Visit
    serializer_class = VisitSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('visit_number')