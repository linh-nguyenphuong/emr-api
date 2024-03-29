# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from appointment.models import Appointment
from user.admin.serializers import UserSerializer

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = (
            'id',
            'patient',
            'physician',
            'appointment_at',
            'status'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
