# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from emr_drug.models import EmrDrug

class EmrDrugSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=20, decimal_places=0)

    class Meta:
        model = EmrDrug
        fields = (
            'id',
            'drug_instruction',
            'drug',
            'quantity',
            'unit_price',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }
