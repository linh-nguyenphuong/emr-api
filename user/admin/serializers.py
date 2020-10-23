# Django imports
from django.conf import settings

# Rest framework imports
from rest_framework import serializers

# Model imports
from user.models import User
from emr.models import Emr

# Serialier imports
from role.user.serializers import RoleSerializer

class UserSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(write_only=True)
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone',
            'password',
            'address',
            'first_name', 
            'last_name', 
            'DOB',
            'role',
            'role_id',
            'is_active',
            'is_verified_email',
            'is_verified_phone',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_verified_email': {'read_only': True},
            'is_verified_phone': {'read_only': True},
        }


class FilterDateRangeFormatSerializer(serializers.Serializer):
    from_date = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d'])
    to_date = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d'])

    class Meta:
        fields = (
            'from_date',
            'to_date',
        )

class ReportPatientSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()

    class Meta:
        model = Emr
        fields = (
            'id',
            'total',
            'created_at',
            'is_paid',
            'patient'
        )

    @staticmethod
    def get_patient(obj):
        return obj.patient.first_name + ' ' + obj.patient.last_name