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
from emr_service.models import EmrService

# Serialier imports
from user.profile.serializers import PublicProfileSerializer
from emr_drug.user.serializers import EmrDrugSerializer
from emr_disease.user.serializers import EmrDiseaseSerializer
from emr_service.user.serializers import EmrServiceSerializer

class EmrImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmrImage
        fields = (
            'id',
            'url'
        )
        extra_kwargs = {
            'id': {'read_only': True},
        }

class EmrSerializer(serializers.ModelSerializer):
    patient = PublicProfileSerializer(read_only=True)
    patient_id = serializers.CharField(write_only=True)

    physician = PublicProfileSerializer(read_only=True)
    physician_id = serializers.CharField(write_only=True)

    emr_drugs = serializers.SerializerMethodField('get_emr_drug')
    emr_diseases = serializers.SerializerMethodField('get_emr_disease')
    emr_services = serializers.SerializerMethodField('get_emr_service')
    images = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Emr
        fields = (
            'id',
            'patient',
            'patient_id',
            'physician',
            'physician_id',
            'emr_diseases',
            'emr_services',
            'emr_drugs',
            'images',
            'created_at',
            'total',
            'status',
            'is_paid'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'emr_drugs': {'read_only': True},
            'emr_diseases': {'read_only': True},
            'emr_services': {'read_only': True},
            'images': {'read_only': True},
            'total': {'read_only': True},
        }

    @staticmethod
    def get_emr_drug(obj):
        emr_drugs = EmrDrug.objects.filter(emr=obj,
                                          is_deleted=False)
        serializer = EmrDrugSerializer(instance=emr_drugs, many=True)                          
        return serializer.data

    @staticmethod
    def get_emr_disease(obj):
        emr_diseases = EmrDisease.objects.filter(emr=obj,
                                                is_deleted=False)
        serializer = EmrDiseaseSerializer(instance=emr_diseases, many=True) 
        return serializer.data

    @staticmethod
    def get_emr_service(obj):
        emr_services = EmrService.objects.filter(emr=obj,
                                                is_deleted=False)
        serializer = EmrServiceSerializer(instance=emr_services, many=True)
        return serializer.data

    @staticmethod
    def get_image(obj):
        images = EmrImage.objects.filter(emr=obj,
                                        is_deleted=False)
        serializer = EmrImageSerializer(instance=images, many=True) 
        return serializer.data