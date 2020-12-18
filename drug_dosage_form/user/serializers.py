# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from drug_dosage_form.models import DrugDosageForm

class DrugDosageFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = DrugDosageForm
        fields = (
            'id',
            'name',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

