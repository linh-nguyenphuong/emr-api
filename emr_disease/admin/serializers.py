# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from emr_disease.models import EmrDisease

class EmrDiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmrDisease
        fields = (
            'id',
            'disease',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
