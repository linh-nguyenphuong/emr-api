# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from drug.models import Drug
from drug_category.user.serializers import DrugCategorySerializer
from drug_unit.user.serializers import DrugUnitSerializer

class DrugSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Drug
        fields = (
            'id',
            'name',
            'code',
            'price',
            'drug_category',
            'drug_unit',
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }


class DrugDetailsSerializer(serializers.ModelSerializer):
    drug_category = DrugCategorySerializer()
    drug_unit = DrugUnitSerializer()

    class Meta:
        model = Drug
        fields = (
            'id',
            'name',
            'code',
            'price',
            'drug_category',
            'drug_unit',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'drug_category': {'read_only': True},
            'drug_unit': {'read_only': True}
        }

