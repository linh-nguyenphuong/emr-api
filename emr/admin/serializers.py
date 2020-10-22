# Django imports

# Rest framework imports
from rest_framework import serializers

# Application imports
from templates.error_template import ErrorTemplate

# Model imports
from emr.models import (
    Emr,
    EmrImage
)
from emr_drug.models import EmrDrug
from emr_disease.models import EmrDisease
from patient_service.models import PatientService

from drug.admin.serializers import DrugSerializer


class EmrSerializer(serializers.ModelSerializer):
    emr_drug = serializers.SerializerMethodField()
    emr_disease = serializers.SerializerMethodField()
    emr_service = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Emr
        fields = (
            'id',
            'patient',
            'physician',
            'emr_drug',
            'emr_disease',
            'emr_service',
            'image',
            'total'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'emr_drug': {'read_only': True},
            'emr_disease': {'read_only': True},
            'image': {'read_only': True},
        }

    @staticmethod
    def get_emr_drug(obj):
        emr_drug = EmrDrug.objects.filter(emr=obj,
                                          is_deleted=False)
        list_drug = []
        for drug in emr_drug:
            list_drug.append(
                dict(
                    id=drug.id,
                    drug=DrugSerializer(drug.drug).data
                ))
        return list_drug

    @staticmethod
    def get_emr_disease(obj):
        emr_disease = EmrDisease.objects.filter(emr=obj,
                                                is_deleted=False)
        list_disease = []
        for data in emr_disease:
            list_disease.append(
                dict(
                    id=data.id,
                    disease=data.disease_id,
                )
            )
        return list_disease

    @staticmethod
    def get_emr_service(obj):
        emr_service = PatientService.objects.filter(emr=obj,
                                                    is_deleted=False)
        list_service = []
        for data in emr_service:
            list_service.append(
                dict(
                    id=data.id,
                    service=data.service.id,
                    name=data.service.name,
                    price=data.service.price
                )
            )
        return list_service

    @staticmethod
    def get_image(obj):
        image = EmrImage.objects.filter(emr=obj,
                                        is_deleted=False)
        if image:
            return image.values()
        return None
