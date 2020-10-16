# Rest framework imports
from rest_framework import serializers

# Model imports
from user.models import User
from role.models import Role


class ListUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'is_verified_email',
            'is_verified_phone',
            'role'
        )

    @staticmethod
    def get_role(instance):
        if instance.role:
            result = dict(
                id=instance.role.id,
                name=instance.role.name
            )
            return result
        return None


class CreateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=191)
    last_name = serializers.CharField(max_length=191)
    email = serializers.EmailField(min_length=3)
    role = serializers.ChoiceField(choices=Role.objects.filter(is_active=True).values_list('id', flat=True))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'role'
        )
