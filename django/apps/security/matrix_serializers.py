from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.security.models import Resource, ResourceRole, Role, RoleUser, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "status", "password", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "description", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class RoleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleUser
        fields = ["id", "role", "user", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["id", "name", "method", "route", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ResourceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceRole
        fields = ["id", "resource", "role", "status", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
