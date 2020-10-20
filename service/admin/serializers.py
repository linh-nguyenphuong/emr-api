# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from service.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    price = serializers.DecimalField(default=0, decimal_places=0, max_digits=20)

    class Meta:
        model = Service
        fields = (
            'id',
            'name',
            'price'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

