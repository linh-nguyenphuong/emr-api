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
from room.models import (
    Room
)

# Serialier imports
from room.admin.serializers import (
    RoomSerializer,
)


# List Role
class RoomView(generics.ListCreateAPIView):
    model = Room
    serializer_class = RoomSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('number')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class RoomDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = Room
    serializer_class = RoomSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'room_id'

    def get(self, request, *args, **kwargs):
        room_id = self.kwargs.get(self.lookup_url_kwarg)
        room = self.get_object(room_id)

        # Get serializer
        serializer = self.serializer_class(instance=room)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        room_id = self.kwargs.get(self.lookup_url_kwarg)
        room = self.get_object(room_id)

        # Get serializer
        serializer = RoomSerializer(room, data=request.data)
        serializer.is_valid(raise_exception=False)
        disease = serializer.save()

        return Response(self.serializer_class(disease).data)

    def delete(self, request, *args, **kwargs):
        room_id = self.kwargs.get(self.lookup_url_kwarg)
        room = self.get_object(room_id)

        room.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        room.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.ROOM_NOT_EXIST)

        return obj