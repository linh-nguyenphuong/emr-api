# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from patient_service.models import PatientService

class EmrServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientService
        fields = (
            'id',
            'service',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
