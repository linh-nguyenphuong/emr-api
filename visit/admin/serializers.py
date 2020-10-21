# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from visit.models import Visit

class VisitSerializer(serializers.ModelSerializer):
    visit_number = serializers.IntegerField()

    class Meta:
        model = Visit
        fields = (
            'id',
            'visit_number',
            'patient',
            'room',
            'created_at'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
