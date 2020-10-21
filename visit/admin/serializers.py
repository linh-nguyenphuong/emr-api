# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from visit.models import Visit

class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = (
            'id',
            'patient',
            'room',
            'created_at',
            'visit_number'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'visit_number': {'read_only': True},
        }
