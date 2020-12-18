# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from drug_route.models import DrugRoute

class DrugRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DrugRoute
        fields = (
            'id',
            'name',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

