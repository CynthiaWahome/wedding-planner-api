"""Serializers for Tasks app - Capstone MVP"""

from rest_framework import serializers

from apps.common.constants import TaskAssignment

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task management"""

    wedding_profile = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = [
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

    def validate_assigned_to(self, value):
        """Validate assignment choice"""
        valid_choices = [choice[0] for choice in TaskAssignment.CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(f"Invalid choice. Must be one of: {valid_choices}")
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks"""

    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "vendor"]

    def validate_assigned_to(self, value):
        valid_choices = [choice[0] for choice in TaskAssignment.CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(f"Invalid choice. Must be one of: {valid_choices}")
        return value

    def create(self, validated_data):
        # Auto-assign to user's wedding profile
        user = self.context["request"].user
        validated_data["wedding_profile"] = user.wedding_profile
        return super().create(validated_data)
