# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from drug_instruction.models import DrugInstruction

class DrugInstructionSerializer(serializers.ModelSerializer):
    instruction = serializers.CharField()

    class Meta:
        model = DrugInstruction
        fields = (
            'id',
            'instruction',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

