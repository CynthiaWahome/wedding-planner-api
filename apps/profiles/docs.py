"""OpenAPI documentation for Wedding Profile endpoints - Capstone MVP."""

from drf_spectacular.openapi import OpenApiExample, OpenApiResponse
from drf_spectacular.utils import extend_schema

from apps.common.errors import get_error_documentation
from apps.common.serializers import StandardSuccessResponseSerializer

from .serializers import WeddingProfileCreateSerializer, WeddingProfileSerializer

COMMON_PROFILE_ERRORS = {
    **get_error_documentation(400),
    **get_error_documentation(401),
    **get_error_documentation(403),
    **get_error_documentation(405),
    **get_error_documentation(500),
}


profile_list_docs = extend_schema(
    summary="List wedding profiles",
    description="Retrieve all wedding profiles for the authenticated user",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding profiles retrieved successfully",
                        "data": [
                            {
                                "id": 1,
                                "user": "wanjiku.kamau@gmail.com",
                                "wedding_date": "2025-12-15",
                                "bride_name": "Wanjiku Kamau",
                                "groom_name": "James Mwangi",
                                "venue": "Safari Park Hotel, Nairobi",
                                "budget": 850000.00,
                                "created_at": "2025-08-26T10:15:30.123456Z",
                                "updated_at": "2025-08-26T14:20:45.654321Z",
                            }
                        ],
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_PROFILE_ERRORS,
    },
)

profile_create_docs = extend_schema(
    summary="Create wedding profile",
    description="Create a new wedding profile for the authenticated user",
    request=WeddingProfileCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding profile created successfully",
                        "data": {
                            "id": 2,
                            "user": "grace.njeri@outlook.com",
                            "wedding_date": "2026-06-20",
                            "bride_name": "Grace Njeri",
                            "groom_name": "Peter Kiprotich",
                            "venue": "Windsor Golf Hotel & Country Club",
                            "budget": 1200000.00,
                            "created_at": "2025-08-26T11:30:15.789123Z",
                            "updated_at": "2025-08-26T11:30:15.789123Z",
                        },
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_PROFILE_ERRORS,
    },
)

profile_retrieve_docs = extend_schema(
    summary="Retrieve wedding profile",
    description="Get wedding profile details by ID",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding profile retrieved successfully",
                        "data": {
                            "id": 1,
                            "user": "wanjiku.kamau@gmail.com",
                            "wedding_date": "2025-12-15",
                            "bride_name": "Wanjiku Kamau",
                            "groom_name": "James Mwangi",
                            "venue": "Safari Park Hotel, Nairobi",
                            "budget": 850000.00,
                            "created_at": "2025-08-26T10:15:30.123456Z",
                            "updated_at": "2025-08-26T14:20:45.654321Z",
                        },
                        "errors": None,
                    },
                )
            ],
        ),
        404: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Not Found",
                    value={
                        "success": False,
                        "message": "Wedding profile not found",
                        "data": None,
                        "errors": {"detail": "Wedding profile not found"},
                    },
                )
            ],
        ),
        **COMMON_PROFILE_ERRORS,
    },
)

profile_update_docs = extend_schema(
    summary="Update wedding profile",
    description="Update wedding profile details",
    request=WeddingProfileSerializer,
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding profile updated successfully",
                        "data": {
                            "id": 1,
                            "user": "wanjiku.kamau@gmail.com",
                            "wedding_date": "2025-12-22",
                            "bride_name": "Wanjiku Kamau",
                            "groom_name": "James Mwangi",
                            "venue": "Villa Rosa Kempinski, Nairobi",
                            "budget": 950000.00,
                            "created_at": "2025-08-26T10:15:30.123456Z",
                            "updated_at": "2025-08-26T15:45:20.987654Z",
                        },
                        "errors": None,
                    },
                )
            ],
        ),
        404: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Not Found",
                    value={
                        "success": False,
                        "message": "Wedding profile not found",
                        "data": None,
                        "errors": {"detail": "Wedding profile not found"},
                    },
                )
            ],
        ),
        **COMMON_PROFILE_ERRORS,
    },
)

profile_delete_docs = extend_schema(
    summary="Delete wedding profile",
    description="Delete wedding profile by ID",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding profile deleted successfully",
                        "data": None,
                        "errors": None,
                    },
                )
            ],
        ),
        404: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Not Found",
                    value={
                        "success": False,
                        "message": "Wedding profile not found",
                        "data": None,
                        "errors": {"detail": "Wedding profile not found"},
                    },
                )
            ],
        ),
        **COMMON_PROFILE_ERRORS,
    },
)
