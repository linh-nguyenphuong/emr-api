# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from notification.models import Notification


class SendNotificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    receivers = serializers.ListField(allow_null=True)

    class Meta:
        model = Notification
        fields = (
            'title',
            'content',
            'receivers',
        )


class NotificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'title',
            'content',
            'is_read',
            'sender',
            'receiver',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'is_read': {'read_only': True},
            'sender': {'read_only': True},
            'receiver': {'read_only': True},

        }

