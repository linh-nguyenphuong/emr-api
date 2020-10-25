# Django imports
from django.conf import settings

# Rest framework imports
from rest_framework import serializers

# Model imports
from user.models import User
from emr.models import Emr

# Serialier imports
from role.user.serializers import RoleSerializer

class PatientSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'password',
            'address',
            'first_name', 
            'last_name', 
            'gender',
            'DOB',
            'role',
            'is_active',
            'is_verified_phone',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_verified_phone': {'read_only': True},
        }
