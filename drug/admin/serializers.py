# Django imports

# Rest framework imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from drug.models import Drug
from drug_category.admin.serializers import DrugCategorySerializer
from drug_unit.admin.serializers import DrugUnitSerializer
from drug_dosage_form.admin.serializers import DrugDosageFormSerializer
from drug_route.admin.serializers import DrugRouteSerializer

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = (
            'id',
            'name',
            'code',
            'price',
            'drug_category',
            'drug_unit',
            'drug_dosage_form',
            'drug_route',
            'strength'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }


class DrugDetailsSerializer(serializers.ModelSerializer):
    drug_category = DrugCategorySerializer()
    drug_unit = DrugUnitSerializer()
    drug_dosage_form = DrugDosageFormSerializer()
    drug_route = DrugRouteSerializer()

    class Meta:
        model = Drug
        fields = (
            'id',
            'name',
            'code',
            'price',
            'drug_category',
            'drug_unit',
            'drug_dosage_form',
            'drug_route',
            'strength'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'drug_category': {'read_only': True},
            'drug_unit': {'read_only': True},
            'drug_dosage_form': {'read_only': True},
            'drug_route': {'read_only': True},
        }

