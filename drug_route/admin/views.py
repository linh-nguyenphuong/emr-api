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
from drug_route.models import (
    DrugRoute
)

# Serialier imports
from drug_route.admin.serializers import (
    DrugRouteSerializer,
)

class DrugRouteView(generics.ListCreateAPIView):
    model = DrugRoute
    serializer_class = DrugRouteSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False).order_by('name')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class DrugRouteDetailsView(generics.RetrieveUpdateDestroyAPIView):
    model = DrugRoute
    serializer_class = DrugRouteSerializer
    permission_classes = (IsAdmin,)
    lookup_url_kwarg = 'drug_route_id'

    def get(self, request, *args, **kwargs):
        drug_route_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_route = self.get_object(drug_route_id)

        # Get serializer
        serializer = self.serializer_class(instance=drug_route)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        drug_route_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_route = self.get_object(drug_route_id)

        # Get serializer
        serializer = self.serializer_class(drug_route, data=request.data)
        serializer.is_valid(raise_exception=False)
        data = request.data

        drug_route.__dict__.update(
            name=data.get('name'),
        )

        # Save to database
        drug_route.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        drug_route_id = self.kwargs.get(self.lookup_url_kwarg)
        drug_route = self.get_object(drug_route_id)

        drug_route.__dict__.update(
            is_deleted=True,
        )

        # Save to database
        drug_route.save()

        return Response({
            'message': 'Deleted successfully'
        })

    def get_object(self, object_id):
        obj = self.model.objects.filter(
            id=object_id,
            is_deleted=False
        ).first()

        if not obj:
            raise ValidationError(ErrorTemplate.DRUG_ROUTE_NOT_EXIST)

        return obj