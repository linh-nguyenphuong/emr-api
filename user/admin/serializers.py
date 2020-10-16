# Django imports
from django.conf import settings

# Rest framework imports
from rest_framework import serializers

# Model imports
from user.models import User

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


