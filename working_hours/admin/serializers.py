# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from working_hours.models import WorkingHours

class WorkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHours
        fields = (
            'id',
            'weekday',
            'is_closed'
        )
        extra_kwargs = {
            'id': {'read_only': True}
        }

