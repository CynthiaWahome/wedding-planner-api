"""Serializers for Wedding Profile app - Capstone MVP."""

from typing import ClassVar

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.profiles.validators import (
    validate_bride_groom_names,
    validate_venue_name,
    validate_wedding_budget_structure,
    validate_wedding_date_range,
)

from .models import WeddingProfile

User = get_user_model()


class WeddingProfileSerializer(serializers.ModelSerializer):
    """Serializer for wedding profile management."""

    user: serializers.StringRelatedField = serializers.StringRelatedField(
        read_only=True
    )
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
        """Validate wedding date meets planning requirements."""
        validate_wedding_date_range(value)
        return value

    def validate_budget(self, value):
        """Validate budget meets wedding requirements."""
        validate_wedding_budget_structure(value)
        return value

    def validate_venue(self, value):
        """Validate venue name format."""
        if value:
            validate_venue_name(value)
        return value

    def validate(self, attrs):
        """Cross-field validation for bride and groom names."""
        bride_name = attrs.get("bride_name")
        groom_name = attrs.get("groom_name")
        if bride_name and groom_name:
            validate_bride_groom_names(bride_name, groom_name)
        return attrs


class WeddingProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating wedding profile."""

    class Meta:
        """Meta configuration for serializer."""

        model = WeddingProfile
        fields: ClassVar = [
            "wedding_date",
            "bride_name",
            "groom_name",
            "venue",
            "budget",
        ]

    def validate_wedding_date(self, value):
        """Validate wedding date meets planning requirements."""
        validate_wedding_date_range(value)
        return value

    def validate_budget(self, value):
        """Validate budget meets wedding requirements."""
        validate_wedding_budget_structure(value)
        return value

    def validate_venue(self, value):
        """Validate venue name format."""
        if value:
            validate_venue_name(value)
        return value

    def validate(self, attrs):
        """Cross-field validation for bride and groom names."""
        bride_name = attrs.get("bride_name")
        groom_name = attrs.get("groom_name")
        if bride_name and groom_name:
            validate_bride_groom_names(bride_name, groom_name)
        return attrs

    def create(self, validated_data):
        """Create instance with auto-assignment."""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
