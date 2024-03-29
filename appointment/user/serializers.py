# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from appointment.models import Appointment

# Serialier imports
from user.profile.serializers import (
    PublicProfileSerializer
)

class AppointmentSerializer(serializers.ModelSerializer):
    patient = PublicProfileSerializer(read_only=True)
    physician = PublicProfileSerializer(read_only=True)

    patient_id = serializers.CharField(write_only=True)
    physician_id = serializers.CharField(write_only=True)

    class Meta:
        model = Appointment
        fields = (
            'id',
            'patient',
            'patient_id',
            'physician',
            'physician_id',
            'appointment_at',
            'status'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'status': {'read_only': True},
        }
