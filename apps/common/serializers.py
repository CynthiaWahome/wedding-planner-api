"""Common serializers for standardized API responses."""

from typing import Any

from rest_framework import serializers


class StandardSuccessResponseSerializer(serializers.Serializer):
    """Standard success response format for API documentation."""

    success = serializers.BooleanField(default=True, help_text="Request success status")
    message = serializers.CharField(help_text="Response message")
    data: Any = serializers.JSONField(help_text="Response data", allow_null=True)
    errors: Any = serializers.JSONField(help_text="Error details", allow_null=True)
