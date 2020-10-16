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


class ListOwnerNotificationSerializer(serializers.ModelSerializer):
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'receiver'
        )

    @staticmethod
    def get_receiver(instance):
        if instance.receiver:
            return instance.receiver.first_name + ' ' + instance.receiver.last_name
        return None