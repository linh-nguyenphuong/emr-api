# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from emr_disease.models import EmrDisease

# Serialier imports
from disease.user.serializers import DiseaseSerializer

class EmrDiseaseSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)
    disease_id = serializers.CharField(write_only=True)

    class Meta:
        model = EmrDisease
        fields = (
            'id',
            'disease',
            'disease_id',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
