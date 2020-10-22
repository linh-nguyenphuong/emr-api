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
from role.models import (
    Role
)

# Serialier imports
from role.user.serializers import (
    RoleSerializer,
)

# List Role
class RoleView(generics.ListAPIView):
    model = Role
    serializer_class = RoleSerializer
    permission_classes = (IsAdmin, )
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.all().order_by('name')

# Retrieve Role
class RoleDetailsView(generics.RetrieveAPIView):
    model = Role
    serializer_class = RoleSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'role_id'

    def get(self, request, *args, **kwargs):
        role_id = self.kwargs.get(self.lookup_url_kwarg)
        role = self.get_object(role_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=role)
        
        return Response(serializer.data)

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.ROLE_NOT_EXIST)

        return obj








