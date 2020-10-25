# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from emr_service.models import EmrService

# Serialier imports
from service.user.serializers import ServiceSerializer

class EmrServiceSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.CharField(write_only=True)

    class Meta:
        model = EmrService
        fields = (
            'id',
            'service',
            'service_id',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
