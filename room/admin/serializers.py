# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from room.models import Room

class RoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    number = serializers.IntegerField()

    class Meta:
        model = Room
        fields = (
            'id',
            'number',
            'name',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

