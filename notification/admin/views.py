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
from notification.models import (
    Notification
)
from user.models import (
    User
)

# Serialier imports
from notification.admin.serializers import (
    NotificationSerializer,
    SendNotificationSerializer
)


# List Role
class NotificationView(generics.ListCreateAPIView):
    model = Notification
    serializer_class = NotificationSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False,
                                         created_at__gte=datetime.now()-timedelta(days=7),
                                         sender=self.request.user
                                         ).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        serializer = SendNotificationSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        fcm = FCMNotification(api_key=settings.FCM_SERVER_KEY)
        for receiver in data['receivers']:
            user = User.objects.filter(id=receiver).first()
            if user.fcm_registration:
                registration_id = user.fcm_registration

                fcm.notify_single_device(
                    registration_id=registration_id,
                    message_title=data['title'],
                    message_body=data['body'],
                    sound="default",
                )
            Notification.objects.create(
                title=data['title'],
                content=data['content'],
                receiver=user,
                sender=self.request.user
            )

        return Response({
            'message': 'Send notice successfully'
        })
