# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from disease_category.models import DiseaseCategory

class DiseaseCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = DiseaseCategory
        fields = (
            'id',
            'name',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

