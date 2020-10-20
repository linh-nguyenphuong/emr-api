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
from setting.models import (
    Setting
)

# Serialier imports
from setting.admin.serializers import (
    SettingsSerializer,
)

# List Role
class SettingView(generics.ListAPIView):
    model = Setting
    serializer_class = SettingsSerializer
    permission_classes = ()
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.all().order_by('attribute')

# Retrieve Role
class SettingDetailsView(generics.RetrieveAPIView, generics.UpdateAPIView):
    model = Setting
    serializer_class = SettingsSerializer
    permission_classes = ()
    lookup_url_kwarg = 'setting_id'

    def get(self, request, *args, **kwargs):
        setting_id = self.kwargs.get(self.lookup_url_kwarg)
        setting = self.get_object(setting_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=setting)
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        setting_id = self.kwargs.get(self.lookup_url_kwarg)
        setting = self.get_object(setting_id)

        # Get serializer
        serializer = self.serializer_class(setting, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        setting.__dict__.update(
            attribute=data.get('attribute'),
            value=data.get('value')
        )

        # Save to database
        setting.save()

        return Response(serializer.data)
    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.ROLE_NOT_EXIST)

        return obj








