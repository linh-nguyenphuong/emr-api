# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from drug_category.models import DrugCategory

class DrugCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = DrugCategory
        fields = (
            'id',
            'name',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

