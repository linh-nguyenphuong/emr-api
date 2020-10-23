# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from emr_service.models import EmrService

class EmrServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmrService
        fields = (
            'id',
            'service',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
