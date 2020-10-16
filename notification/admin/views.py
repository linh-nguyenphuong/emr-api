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
    CreateNotificationSerializer,
    ListOwnerNotificationSerializer
)


class CreateNotificationView(generics.CreateAPIView):
    model = Notification
    serializer_class = CreateNotificationSerializer
    permission_classes = (IsAdmin,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        receives = data['receives']
        for receive in receives:
            user = User.objects.filter(id=receive,
                                       is_active=True).first()
            Notification.objects.create(title=data['title'],
                                        content=data['content'],
                                        receiver=user,
                                        sender=self.request.user)

            fcm = FCMNotification(api_key=settings.FCM_SERVER_KEY)

            fcm.notify_single_device(
                registration_id=user.fcm_registration,
                message_title=data['title'],
                message_body=data['content'],
                sound="default",
            )
        return Response({
            'message': True
        })


class ListOwnerNotificationView(generics.ListAPIView):
    model = Notification
    serializer_class = ListOwnerNotificationSerializer
    permission_classes = (IsAdmin,)

    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)
