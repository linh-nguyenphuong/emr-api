# Python imports
from datetime import datetime, timedelta
from pyfcm import FCMNotification

# Django imports
from django.core.mail import send_mail
from django.conf import settings

# Django REST framework imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import (
    ValidationError,
)
from rest_framework.pagination import PageNumberPagination

# Application imports
from templates.error_template import (
    ErrorTemplate,
)
from api.permissions import (
    IsAdmin
)
from templates.email_template import (
    EmailTemplate
)


# Model imports
from user.models import User
from notification.models import Notification

# Serializer imports
from .serializers import (
    CreateUserSerializer,
    ListUserSerializer,
)


class ListCreateUserView(generics.ListCreateAPIView):
    model = User
    serializer_class = ListUserSerializer
    permission_classes = (IsAdmin,)

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return Response({
            'message': True
        })


class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    model = Notification
    serializer_class = ListOwnerNotificationSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)
