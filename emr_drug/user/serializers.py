# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from emr_drug.models import EmrDrug

# Serialier imports
from drug_instruction.user.serializers import DrugInstructionSerializer
from drug.user.serializers import DrugDetailsSerializer

class EmrDrugSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    drug_instruction = DrugInstructionSerializer(read_only=True)
    drug_instruction_id = serializers.CharField(write_only=True)

    drug = DrugDetailsSerializer(read_only=True)
    drug_id = serializers.CharField(write_only=True)

    class Meta:
        model = EmrDrug
        fields = (
            'id',
            'drug_instruction',
            'drug_instruction_id',
            'drug',
            'drug_id',
            'quantity',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
