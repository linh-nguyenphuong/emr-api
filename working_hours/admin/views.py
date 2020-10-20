# Django imports
from django.utils import timezone

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
from working_hours.models import (
    WorkingHours
)

# Serialier imports
from working_hours.admin.serializers import (
    WorkingSerializer,
)

# List Role
class WorkingView(generics.ListAPIView):
    model = WorkingHours
    serializer_class = WorkingSerializer
    permission_classes = ()
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.all().order_by('weekday')

# Retrieve Role
class WorkingDetailsView(generics.RetrieveAPIView, generics.UpdateAPIView):
    model = WorkingHours
    serializer_class = WorkingSerializer
    permission_classes = ()
    lookup_url_kwarg = 'working_id'

    def get(self, request, *args, **kwargs):
        working_id = self.kwargs.get(self.lookup_url_kwarg)
        working = self.get_object(working_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=working)
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        working_id = self.kwargs.get(self.lookup_url_kwarg)
        working = self.get_object(working_id)

        # Get serializer
        serializer = self.serializer_class(working, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        working.__dict__.update(
            weekday=data.get('weekday'),
            is_closed=data.get('is_closed')
        )

        # Save to database
        working.save()

        return Response(serializer.data)
    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.WORKING_NOT_EXIST)

        return obj








