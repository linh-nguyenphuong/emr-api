# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from setting.models import Setting

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = (
            'id',
            'attribute',
            'value'
        )
        extra_kwargs = {
            'id': {'read_only': True}
        }

