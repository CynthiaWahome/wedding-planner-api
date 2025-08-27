"""Serializers for Vendors app - Capstone MVP."""

from typing import ClassVar

from rest_framework import serializers

from apps.vendors.validators import (
    validate_vendor_category,
    validate_vendor_contact_info,
    validate_vendor_name,
)

from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for vendor management."""

    wedding_profile: serializers.StringRelatedField = serializers.StringRelatedField(
        read_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta configuration for serializer."""

        model = Vendor
        fields: ClassVar = [
            "id",
            "wedding_profile",
            "name",
            "category",
            "contact_person",
            "phone",
            "email",
            "notes",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        """Validate vendor name format."""
        validate_vendor_name(value)
        return value

    def validate_phone(self, value):
        """Validate vendor phone number."""
        if value:
            validate_vendor_contact_info("phone", value)
        return value

    def validate_email(self, value):
        """Validate vendor email."""
        if value:
            validate_vendor_contact_info("email", value)
        return value

    def validate_category(self, value):
        """Validate vendor category choice."""
        validate_vendor_category(value)
        return value


class VendorCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating vendors."""

    class Meta:
        """Meta configuration for serializer."""

        model = Vendor
        fields: ClassVar = [
            "name",
            "category",
            "contact_person",
            "phone",
            "email",
            "notes",
        ]

    def validate_name(self, value):
        """Validate vendor name format."""
        validate_vendor_name(value)
        return value

    def validate_phone(self, value):
        """Validate vendor phone number."""
        if value:
            validate_vendor_contact_info("phone", value)
        return value

    def validate_email(self, value):
        """Validate vendor email."""
        if value:
            validate_vendor_contact_info("email", value)
        return value

    def validate_category(self, value):
        """Validate category field."""
        validate_vendor_category(value)
        return value

    def create(self, validated_data):
        """Create instance with auto-assignment."""
        user = self.context["request"].user
        validated_data["wedding_profile"] = user.wedding_profile
        return super().create(validated_data)
