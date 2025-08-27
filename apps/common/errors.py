"""Synchronized error responses - runtime and documentation always match."""

from typing import Any

from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from rest_framework import serializers, status

from .responses import APIResponse

ERROR_TEMPLATES = {
    400: {
        "message": "Bad Request - Invalid data format",
        "errors": ["Required field is missing", "Invalid data format provided"],
    },
    401: {
        "message": "Authentication credentials were not provided",
        "errors": ["Authorization header missing or invalid JWT token"],
    },
    403: {
        "message": "You do not have permission to perform this action",
        "errors": ["Access denied to this resource"],
    },
    404: {
        "message": "Resource not found",
        "errors": ["The requested resource does not exist"],
    },
    405: {
        "message": "Method not allowed",
        "errors": ["This HTTP method is not supported for this endpoint"],
    },
    422: {
        "message": "Unprocessable Entity - Business logic validation failed",
        "errors": ["Data is valid but violates business rules"],
    },
    500: {
        "message": "Internal server error occurred",
        "errors": ["An unexpected error occurred. Please try again later"],
    },
}


class StandardErrors:
    """Runtime error responses - always matches documentation."""

    @staticmethod
    def bad_request(message=None, errors=None):
        """400 Bad Request."""
        template = ERROR_TEMPLATES[400]
        return APIResponse.error(
            message=message or template["message"],
            errors=errors or template["errors"],
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def unauthorized(message=None, errors=None):
        """401 Unauthorized."""
        template = ERROR_TEMPLATES[401]
        return APIResponse.error(
            message=message or template["message"],
            errors=errors or template["errors"],
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    @staticmethod
    def forbidden(message=None, errors=None):
        """403 Forbidden."""
        template = ERROR_TEMPLATES[403]
        return APIResponse.error(
            message=message or template["message"],
            errors=errors or template["errors"],
            status_code=status.HTTP_403_FORBIDDEN,
        )

    @staticmethod
    def not_found(message=None, errors=None):
        """404 Not Found."""
        template = ERROR_TEMPLATES[404]
        return APIResponse.error(
            message=message or template["message"],
            errors=errors or template["errors"],
            status_code=status.HTTP_404_NOT_FOUND,
        )

    @staticmethod
    def method_not_allowed(message=None, errors=None):
        """405 Method Not Allowed."""
        template = ERROR_TEMPLATES[405]
        return APIResponse.error(
            message=message or template["message"],
            errors=errors or template["errors"],
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @staticmethod
    def validation_error(errors, message=None):
        """422 Unprocessable Entity."""
        template = ERROR_TEMPLATES[422]
        return APIResponse.error(
            message=message or template["message"],
            errors=errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @staticmethod
    def internal_server_error(message=None, errors=None):
        """500 Internal Server Error."""
        template = ERROR_TEMPLATES[500]
        return APIResponse.error(
            message=message or template["message"],
            errors=errors or template["errors"],
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class ErrorResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(
        default=False, help_text="Always false for errors"
    )
    message = serializers.CharField(help_text="Error message")
    data: Any = serializers.JSONField(
        allow_null=True, default=None, help_text="Always null for errors"
    )
    errors: Any = serializers.ListField(
        child=serializers.CharField(), help_text="List of specific error messages"
    )


def get_error_documentation(
    status_code: int,
    custom_message: str | None = None,
    custom_errors: list[Any] | None = None,
) -> dict[str, Any]:
    """Generate OpenAPI documentation that matches runtime responses exactly."""
    template = ERROR_TEMPLATES.get(status_code, ERROR_TEMPLATES[500])

    response_example = {
        "success": False,
        "message": custom_message or template["message"],
        "data": None,
        "errors": custom_errors or template["errors"],
    }

    return {
        status_code: OpenApiResponse(
            response=ErrorResponseSerializer,
            description="",
            examples=[
                OpenApiExample(
                    f"Error {status_code}",
                    summary=f"Standard {status_code} error response",
                    value=response_example,
                )
            ],
        )
    }


COMMON_AUTH_ERRORS = {
    **get_error_documentation(401),
    **get_error_documentation(403),
    **get_error_documentation(500),
}

COMMON_CRUD_ERRORS = {
    **get_error_documentation(400),
    **get_error_documentation(401),
    **get_error_documentation(403),
    **get_error_documentation(404),
    **get_error_documentation(500),
}

COMMON_CREATE_ERRORS = {
    **get_error_documentation(400),
    **get_error_documentation(401),
    **get_error_documentation(403),
    **get_error_documentation(500),
}
