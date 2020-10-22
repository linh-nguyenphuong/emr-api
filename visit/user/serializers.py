# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from visit.models import Visit

# Serialier imports
from user.profile.serializers import (
    PublicProfileSerializer
)
from room.user.serializers import (
    RoomSerializer
)

class VisitSerializer(serializers.ModelSerializer):
    patient = PublicProfileSerializer(read_only=True)
    patient_id = serializers.CharField(write_only=True)

    room = RoomSerializer(read_only=True)
    room_id = serializers.CharField(write_only=True)

    class Meta:
        model = Visit
        fields = (
            'id',
            'patient',
            'patient_id',
            'room',
            'room_id',
            'created_at',
            'visit_number'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'visit_number': {'read_only': True},
        }
