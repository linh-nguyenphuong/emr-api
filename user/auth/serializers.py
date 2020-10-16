# Django imports
from django.conf import settings

# Rest framework imports
from rest_framework import serializers

# Model imports
from user.models import User

class VerifyEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name', 
            'last_name', 
            'is_verified_email'
        )
        extra_kwargs = {
            'email': {'read_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'is_verified_email': {'read_only': True},
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        fields = (
            'old_password',
            'new_password',
            'confirm_password',
        )


