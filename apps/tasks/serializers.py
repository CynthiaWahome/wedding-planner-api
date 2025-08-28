"""Serializers for Tasks app - Capstone MVP."""

from typing import ClassVar

from rest_framework import serializers

from apps.common.constants import TaskAssignment
from apps.tasks.validators import (
    validate_task_description,
    validate_task_title,
)

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task management."""

    wedding_profile: serializers.StringRelatedField = serializers.StringRelatedField(
        read_only=True
    )
    vendor: serializers.StringRelatedField = serializers.StringRelatedField(
        read_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta configuration for serializer."""

        model = Task
        fields: ClassVar = [
            "id",
            "wedding_profile",
            "title",
            "description",
            "assigned_to",
            "is_completed",
            "vendor",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        """Validate task title format."""
        validate_task_title(value)
        return value

    def validate_description(self, value):
        """Validate task description."""
        validate_task_description(value)
        return value

    def validate_assigned_to(self, value):
        """Validate assignment choice."""
        valid_choices = [choice[0] for choice in TaskAssignment.CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid choice. Must be one of: {valid_choices}"
            )
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks."""

    class Meta:
        """Meta configuration for serializer."""

        model = Task
        fields: ClassVar = ["title", "description", "assigned_to", "vendor"]

    def validate_title(self, value):
        """Validate task title format."""
        validate_task_title(value)
        return value

    def validate_description(self, value):
        """Validate task description."""
        validate_task_description(value)
        return value

    def validate_assigned_to(self, value):
        """Validate assigned_to field."""
        valid_choices = [choice[0] for choice in TaskAssignment.CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid choice. Must be one of: {valid_choices}"
            )
        return value

    def create(self, validated_data):
        """Create instance with auto-assignment to user's wedding profile."""
        user = self.context["request"].user
        validated_data["wedding_profile"] = user.wedding_profile
        return super().create(validated_data)


class TaskToggleSerializer(serializers.Serializer):
    """Serializer for task completion toggle operation."""

    pass
