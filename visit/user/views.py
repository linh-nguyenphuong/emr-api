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
    IsPhysicianOrReceptionist
)

# Model imports
from visit.models import (
    Visit
)
from user.models import (
    User
)
from room.models import (
    Room
)

# Serialier imports
from visit.user.serializers import (
    VisitSerializer,
)

class VisitView(generics.ListCreateAPIView):
    model = Visit
    serializer_class = VisitSerializer
    permission_classes = (IsPhysicianOrReceptionist,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = (
        'visit_number',
        'patient__first_name',
        'patient__last_name'
    )
    filter_fields = {
        'room_id': ['exact'],
        'created_at': ['gte', 'lte', 'exact']
    }

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('visit_number')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check patient exist
        patient = User.objects.filter(
            id=data.get('patient_id'),
            is_deleted=False,
            role__name='patient'
        ).first()
        if not patient:
            raise ValidationError(ErrorTemplate.PATIENT_NOT_EXIST)

        # Check room exist
        room = Room.objects.filter(
            id=data.get('room_id'),
            is_deleted=False,
        ).first()
        if not room:
            raise ValidationError(ErrorTemplate.ROOM_NOT_EXIST)

        visit = self.model.objects.filter(
            room=room,
            created_at__day=datetime.now().day,
            created_at__month=datetime.now().month,
            created_at__year=datetime.now().year
        ).order_by('-visit_number').first()
        
        current_number = 1
        if visit:
            current_number = visit.visit_number + 1

        serializer.save(
            created_by=self.request.user,
            visit_number=current_number
        )

        return Response(serializer.data)

class VisitDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Visit
    serializer_class = VisitSerializer
    permission_classes = (IsPhysicianOrReceptionist,)
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

        # Check patient exist
        patient = User.objects.filter(
            id=data.get('patient_id'),
            is_deleted=False,
            role__name='patient'
        ).first()
        if not patient:
            raise ValidationError(ErrorTemplate.PATIENT_NOT_EXIST)

        visit = serializer.save()
        
        return Response(self.serializer_class(visit).data)

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


class PrintView(generics.ListAPIView):
    model = Visit
    serializer_class = VisitSerializer
    permission_classes = (IsPhysicianOrReceptionist,)
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('visit_number')