"""Serializers for Guests app - Capstone MVP."""

from typing import ClassVar

from rest_framework import serializers

from apps.guests.validators import (
    validate_guest_email_format,
    validate_guest_name,
    validate_rsvp_status,
)

from .models import Guest


class GuestSerializer(serializers.ModelSerializer):
    """Serializer for guest management."""

    wedding_profile: serializers.StringRelatedField = serializers.StringRelatedField(
        read_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta configuration for serializer."""

        model = Guest
        fields: ClassVar = [
            "id",
            "wedding_profile",
            "name",
            "email",
            "rsvp_status",
            "plus_one",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        """Validate guest name format."""
        validate_guest_name(value)
        return value

    def validate_email(self, value):
        """Validate guest email format."""
        validate_guest_email_format(value)
        return value

    def validate_rsvp_status(self, value):
        """Validate RSVP status choice."""
        validate_rsvp_status(value)
        return value


class GuestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating guests."""

    class Meta:
        """Meta configuration for serializer."""

        model = Guest
        fields: ClassVar = ["name", "email", "rsvp_status", "plus_one"]

    def validate_name(self, value):
        """Validate guest name format."""
        validate_guest_name(value)
        return value

    def validate_email(self, value):
        """Validate guest email format."""
        validate_guest_email_format(value)
        return value

    def validate_rsvp_status(self, value):
        """Validate RSVP status choice."""
        validate_rsvp_status(value)
        return value

    def create(self, validated_data):
        """Create instance with auto-assignment to user's wedding profile."""
        user = self.context["request"].user
        validated_data["wedding_profile"] = user.wedding_profile
        return super().create(validated_data)
