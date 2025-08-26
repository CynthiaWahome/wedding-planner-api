"""Serializers for Authentication app."""

from typing import ClassVar

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        """Meta class for user registration serializer."""

        model = User
        fields: ClassVar = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Validate credentials."""
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            try:
                user_obj = User.objects.get(username=username)
                if not user_obj.check_password(password):
                    raise serializers.ValidationError("Invalid credentials")
                if not user_obj.is_active:
                    raise serializers.ValidationError("User account is disabled")

                attrs["user"] = user_obj
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid credentials") from None
        else:
            raise serializers.ValidationError("Must include username and password")

        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile information."""

    class Meta:
        """Meta class for user serializer."""

        model = User
        fields: ClassVar = ["id", "username", "email", "first_name", "last_name", "date_joined"]
        read_only_fields: ClassVar = ["id", "username", "date_joined"]
