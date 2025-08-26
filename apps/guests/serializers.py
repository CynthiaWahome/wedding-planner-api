"""Serializers for Guests app - Capstone MVP."""

from typing import ClassVar

from rest_framework import serializers

from apps.common.constants import RSVPStatus

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

    def validate_rsvp_status(self, value):
        """Validate RSVP status choice."""
        valid_choices = [choice[0] for choice in RSVPStatus.CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid choice. Must be one of: {valid_choices}"
            )
        return value


class GuestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating guests."""

    class Meta:
        """Meta configuration for serializer."""

        model = Guest
        fields: ClassVar = ["name", "email", "rsvp_status", "plus_one"]

    def validate_rsvp_status(self, value):
        """Validate rsvp_status field."""
        valid_choices = [choice[0] for choice in RSVPStatus.CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid choice. Must be one of: {valid_choices}"
            )
        return value

    def create(self, validated_data):
        """Create instance with auto-assignment."""
        # Auto-assign to user's wedding profile
        user = self.context["request"].user
        validated_data["wedding_profile"] = user.wedding_profile
        return super().create(validated_data)
