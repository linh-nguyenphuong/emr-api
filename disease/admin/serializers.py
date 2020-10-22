# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from disease.models import Disease
from disease_category.admin.serializers import DiseaseCategorySerializer

class DiseaseSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Disease
        fields = (
            'id',
            'name',
            'code',
            'disease_category',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }


class DiseaseDetailsSerializer(serializers.ModelSerializer):
    disease_category = DiseaseCategorySerializer()

    class Meta:
        model = Disease
        fields = (
            'id',
            'name',
            'code',
            'disease_category',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'disease_category': {'read_only': True},
        }

