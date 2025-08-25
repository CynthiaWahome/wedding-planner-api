"""Consistent API Response Format for Wedding Planner API.

Ensures all endpoints return responses in the same structure.
"""

from typing import Any

from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    """Standardized API response format for consistent client experience.

    Response Structure:
    {
        "success": true/false,
        "message": "Human readable message",
        "data": {...},  # Response payload
        "errors": [...],  # Validation errors (if any)
        "meta": {...}   # Pagination, etc.
    }
    """

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operation completed successfully",
        status_code: int = status.HTTP_200_OK,
        meta: dict | None = None,
    ) -> Response:
        """Return a standard success response."""
        response_data = {
            "success": True,
            "message": message,
            "data": data,
        }

        if meta:
            response_data["meta"] = meta

        return Response(response_data, status=status_code)

    @staticmethod
    def created(
        data: Any = None, message: str = "Resource created successfully", meta: dict | None = None
    ) -> Response:
        """Return a standard creation response."""
        return APIResponse.success(
            data=data, message=message, status_code=status.HTTP_201_CREATED, meta=meta
        )

    @staticmethod
    def error(
        message: str = "An error occurred",
        errors: list | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Any = None,
    ) -> Response:
        """Return a standard error response."""
        response_data = {
            "success": False,
            "message": message,
            "data": data,
        }

        if errors:
            response_data["errors"] = errors

        return Response(response_data, status=status_code)

    @staticmethod
    def not_found(message: str = "Resource not found", data: Any = None) -> Response:
        """Return a standard 404 response."""
        return APIResponse.error(message=message, status_code=status.HTTP_404_NOT_FOUND, data=data)

    @staticmethod
    def unauthorized(message: str = "Unauthorized access") -> Response:
        """Return a standard 401 response."""
        return APIResponse.error(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden(message: str = "Access forbidden") -> Response:
        """Return a standard 403 response."""
        return APIResponse.error(message=message, status_code=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def validation_error(errors: list, message: str = "Validation failed") -> Response:
        """Return a standard validation error response."""
        return APIResponse.error(
            message=message, errors=errors, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    @staticmethod
    def paginated_response(
        data: list,
        page: int,
        per_page: int,
        total: int,
        message: str = "Data retrieved successfully",
    ) -> Response:
        """Return a standard paginated response."""
        total_pages = (total + per_page - 1) // per_page

        meta = {
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            }
        }

        return APIResponse.success(data=data, message=message, meta=meta)
