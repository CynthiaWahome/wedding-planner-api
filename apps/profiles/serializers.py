"""Serializers for Wedding Profile app - Capstone MVP."""

from typing import ClassVar

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.common.validators.base import (
    validate_future_date,
    validate_positive_amount,
)

from .models import WeddingProfile

User = get_user_model()


class WeddingProfileSerializer(serializers.ModelSerializer):
    """Serializer for wedding profile management."""

    user = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta configuration for serializer."""

        model = WeddingProfile
        fields: ClassVar = [
            "id",
            "user",
            "wedding_date",
            "bride_name",
            "groom_name",
            "venue",
            "budget",
            "created_at",
            "updated_at",
        ]

    def validate_wedding_date(self, value):
        """Validate wedding date is in the future."""
        validate_future_date(value)
        return value

    def validate_budget(self, value):
        """Validate budget is positive if provided."""
        if value is not None:
            validate_positive_amount(value)
        return value


class WeddingProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating wedding profile."""

    class Meta:
        """Meta configuration for serializer."""

        model = WeddingProfile
        fields: ClassVar = ["wedding_date", "bride_name", "groom_name", "venue", "budget"]

    def validate_wedding_date(self, value):
        """Validate wedding date is in the future."""
        validate_future_date(value)
        return value

    def validate_budget(self, value):
        """Validate budget is positive if provided."""
        if value is not None:
            validate_positive_amount(value)
        return value

    def create(self, validated_data):
        """Create instance with auto-assignment."""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
