"""OpenAPI documentation for Vendor Management endpoints - Capstone MVP."""

from drf_spectacular.openapi import OpenApiExample, OpenApiResponse
from drf_spectacular.utils import extend_schema

from apps.common.errors import get_error_documentation
from apps.common.serializers import StandardSuccessResponseSerializer

from .serializers import VendorCreateSerializer, VendorSerializer

COMMON_VENDOR_ERRORS = {
    **get_error_documentation(400),
    **get_error_documentation(401),
    **get_error_documentation(403),
    **get_error_documentation(405),
    **get_error_documentation(500),
}


vendor_list_docs = extend_schema(
    summary="List wedding vendors",
    description="Retrieve all wedding vendors for the authenticated user",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding vendors retrieved successfully",
                        "data": [
                            {
                                "id": 1,
                                "wedding_profile": "wanjiku.kamau@gmail.com",
                                "name": "Safari Park Hotel",
                                "category": "venue",
                                "contact_person": "Susan Wanjiru",
                                "phone": "+254701234567",
                                "email": "events@safaripark.co.ke",
                                "notes": "Reception venue - Garden view. Capacity 200.",
                                "created_at": "2025-08-26T16:00:00.123456Z",
                                "updated_at": "2025-08-26T16:00:00.123456Z",
                            },
                            {
                                "id": 2,
                                "wedding_profile": "wanjiku.kamau@gmail.com",
                                "name": "Marula Studios",
                                "category": "photography",
                                "contact_person": "David Kiprotich",
                                "phone": "+254722345678",
                                "email": "info@marulastudios.co.ke",
                                "notes": "Photography and videography package.",
                                "created_at": "2025-08-26T17:00:15.789123Z",
                                "updated_at": "2025-08-26T17:00:15.789123Z",
                            },
                        ],
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_VENDOR_ERRORS,
    },
)

vendor_create_docs = extend_schema(
    summary="Create wedding vendor",
    description="Add a new wedding vendor for the authenticated user",
    request=VendorCreateSerializer,
    responses={
        201: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding vendor created successfully",
                        "data": {
                            "id": 3,
                            "wedding_profile": "grace.njeri@outlook.com",
                            "name": "DJ Spinmaster Entertainment",
                            "category": "music",
                            "contact_person": "Michael Otieno",
                            "phone": "+254712987654",
                            "email": "dj@spinmaster.co.ke",
                            "notes": "Professional DJ with sound system and lighting",
                            "created_at": "2025-08-26T19:15:30.789123Z",
                            "updated_at": "2025-08-26T19:15:30.789123Z",
                        },
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_VENDOR_ERRORS,
    },
)

vendor_retrieve_docs = extend_schema(
    summary="Retrieve wedding vendor",
    description="Get wedding vendor details by ID",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding vendor retrieved successfully",
                        "data": {
                            "id": 1,
                            "wedding_profile": "wanjiku.kamau@gmail.com",
                            "name": "Safari Park Hotel",
                            "category": "venue",
                            "contact_person": "Susan Wanjiru",
                            "phone": "+254701234567",
                            "email": "events@safaripark.co.ke",
                            "notes": "Reception venue - Garden view. Capacity 200.",
                            "created_at": "2025-08-26T16:00:00.123456Z",
                            "updated_at": "2025-08-26T16:00:00.123456Z",
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
                        "message": "Wedding vendor not found",
                        "data": None,
                        "errors": {"detail": "Wedding vendor not found"},
                    },
                )
            ],
        ),
        **COMMON_VENDOR_ERRORS,
    },
)

vendor_update_docs = extend_schema(
    summary="Update wedding vendor",
    description="Update wedding vendor details",
    request=VendorSerializer,
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding vendor updated successfully",
                        "data": {
                            "id": 1,
                            "wedding_profile": "wanjiku.kamau@gmail.com",
                            "name": "Safari Park Hotel",
                            "category": "venue",
                            "contact_person": "Grace Wanjiru",
                            "phone": "+254701234567",
                            "email": "grace@safaripark.co.ke",
                            "notes": "Reception venue - Garden view. Final quote.",
                            "created_at": "2025-08-26T16:00:00.123456Z",
                            "updated_at": "2025-08-26T20:30:15.987654Z",
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
                        "message": "Wedding vendor not found",
                        "data": None,
                        "errors": {"detail": "Wedding vendor not found"},
                    },
                )
            ],
        ),
        **COMMON_VENDOR_ERRORS,
    },
)

vendor_delete_docs = extend_schema(
    summary="Delete wedding vendor",
    description="Delete wedding vendor by ID",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding vendor deleted successfully",
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
                        "message": "Wedding vendor not found",
                        "data": None,
                        "errors": {"detail": "Wedding vendor not found"},
                    },
                )
            ],
        ),
        **COMMON_VENDOR_ERRORS,
    },
)
