"""Serializers for Vendors app - Capstone MVP"""

from rest_framework import serializers

from apps.common.constants import VendorCategory

from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    """Serializer for vendor management"""

    wedding_profile = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Vendor
        fields = [
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

    def validate_category(self, value):
        """Validate vendor category choice"""
        valid_choices = [choice[0] for choice in VendorCategory.CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(f"Invalid choice. Must be one of: {valid_choices}")
        return value


class VendorCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating vendors"""

    class Meta:
        model = Vendor
        fields = ["name", "category", "contact_person", "phone", "email", "notes"]

    def validate_category(self, value):
        valid_choices = [choice[0] for choice in VendorCategory.CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(f"Invalid choice. Must be one of: {valid_choices}")
        return value

    def create(self, validated_data):
        # Auto-assign to user's wedding profile
        user = self.context["request"].user
        validated_data["wedding_profile"] = user.wedding_profile
        return super().create(validated_data)
