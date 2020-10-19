# Django imports
from django.conf import settings

# Rest framework imports
from rest_framework import serializers

# Model imports
from user.models import User

# Serialier imports
from role.user.serializers import RoleSerializer

class PublicProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'role',
            'avatar'
        )

class PrivateProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone',
            'address',
            'first_name', 
            'last_name', 
            'DOB',
            'avatar',
            'role',
            'is_active',
            'is_verified_email',
            'is_verified_phone',
        )
        extra_kwargs = {
            'email': {'read_only': True},
            'phone': {'read_only': True},
            'is_verified_email': {'read_only': True},
            'is_verified_phone': {'read_only': True},
        }
