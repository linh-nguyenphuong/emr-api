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
            'phone',
            'address',
            'first_name', 
            'last_name',
            'gender', 
            'DOB',
            'avatar',
            'role',
            'job',
            'ethnicity',
            'expatriate',
            'workplace',
            'family_member_name',
            'family_member_address'
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
            'gender', 
            'DOB',
            'avatar',
            'role',
            'is_active',
            'is_verified_email',
            'is_verified_phone',
            'job',
            'ethnicity',
            'expatriate',
            'workplace',
            'family_member_name',
            'family_member_address'
        )
        extra_kwargs = {
            'email': {'read_only': True},
            'phone': {'read_only': True},
            'is_verified_email': {'read_only': True},
            'is_verified_phone': {'read_only': True},
        }
