# Django imports
from django.utils import timezone
from django_filters.rest_framework import (
    DjangoFilterBackend,
)

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
from rest_framework.filters import OrderingFilter, SearchFilter

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

# Serializer imports
from .serializers import (
    RoleSerializer
)


# List - Create Flower Category
class ListCreateRoleView(generics.ListCreateAPIView):
    model = Role
    serializer_class = RoleSerializer
    permission_classes = ()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter,)
    search_fields = (
        'name',
    )
    filter_fields = (
        'name',
    )
    ordering_fields = (
        'name',
    )

    def get_queryset(self):
        return self.model.objects.filter(
            # is_deleted=False
        ).order_by('name')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        is_existed = self.model.objects.filter(
            name=data.get('name'),
            # is_deleted=False
        ).exists()
        if is_existed:
            return Response(ErrorTemplate.ROLE_EXIST, status.HTTP_400_BAD_REQUEST)

        # Save object
        serializer.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

# Retrieve - Update - Delete Flower Category
class DetailUpdateDestroyRoleView(generics.RetrieveUpdateDestroyAPIView):
    model = Role
    serializer_class = RoleSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'role_id'

    def get(self, request, *args, **kwargs):
        flower_category_id = self.kwargs.get(self.lookup_url_kwarg)
        flower_category = self.get_object(flower_category_id)
        
        # Get serializer
        serializer = self.serializer_class(instance=flower_category)
        
        return Response({
            'success': True,
            'data': serializer.data
        })

    def put(self, request, *args, **kwargs):
        flower_category_id = self.kwargs.get(self.lookup_url_kwarg)
        flower_category = self.get_object(flower_category_id)
        
        # Get serializer
        serializer = self.serializer_class(flower_category, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Check Flower Category exists
        flower_category_is_existed = self.model.objects.filter(
            name=data.get('name'),
            is_deleted=False
        ).exclude(id=flower_category_id).exists()
        if flower_category_is_existed:
            raise ValidationError(ErrorTemplate.AdminError.FLOWER_CATEGORY_ALREADY_EXISTED)

        # Save object
        serializer.save()

        return Response({
            'success': True,
            'data': serializer.data
        })

    def delete(self, request, *args, **kwargs):
        flower_category_id = self.kwargs.get(self.lookup_url_kwarg)
        flower_category = self.get_object(flower_category_id)

        flower_category.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        flower_category.save()

        return Response({
            'success': True
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.AdminError.FLOWER_CATEGORY_NOT_EXIST)

        return obj








