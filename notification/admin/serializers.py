# Rest framework imports
from rest_framework import serializers

# Model imports
from user.models import User
from notification.models import Notification


class CreateNotificationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=191)
    receives = serializers.ListField(
        child=serializers.ChoiceField(choices=User.objects.filter(is_active=True).values_list('id', flat=True)),
        allow_null=True,
        allow_empty=True,
    )

    class Meta:
        model = Notification
        fields = (
            'title',
            'content',
            'receives'
        )