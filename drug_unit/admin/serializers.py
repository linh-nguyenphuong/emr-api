# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from drug_unit.models import DrugUnit

class DrugUnitSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = DrugUnit
        fields = (
            'id',
            'name',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

