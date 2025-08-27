"""OpenAPI documentation for Vendor Management endpoints - Capstone MVP."""

from drf_spectacular.openapi import OpenApiExample, OpenApiParameter, OpenApiResponse
from drf_spectacular.utils import extend_schema

from apps.common.errors import get_error_documentation
from apps.common.serializers import StandardSuccessResponseSerializer

from .serializers import VendorCreateSerializer

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
                                "wedding_profile": "aisha.vincent@gmail.com",
                                "name": "Safari Park Hotel",
                                "category": "venue",
                                "contact_person": "Lomokol Akiru",
                                "phone": "+254701234567",
                                "email": "events@safaripark.co.ke",
                                "notes": "Reception venue with garden view!",
                                "created_at": "2025-08-26T16:00:00.123456Z",
                                "updated_at": "2025-08-26T16:00:00.123456Z",
                            },
                            {
                                "id": 2,
                                "wedding_profile": "aisha.vincent@gmail.com",
                                "name": "Event House Kenya",
                                "category": "photography",
                                "contact_person": "Baraka Omondi",
                                "phone": "+254722345678",
                                "email": "bookings@eventhouse.co.ke",
                                "notes": "They make every moment look cinematic!",
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
    examples=[
        OpenApiExample(
            name="Create Vendor Request",
            value={
                "name": "DJ Spinmaster Entertainment",
                "category": "music",
                "contact_person": "Michael Otieno",
                "phone": "+254712987654",
                "email": "dj@spinmaster.co.ke",
                "notes": "Professional DJ with sound system and lighting",
            },
            request_only=True,
        )
    ],
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
                            "wedding_profile": "aisha.vincent@gmail.com",
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
    request=VendorCreateSerializer,
    examples=[
        OpenApiExample(
            name="Update Vendor Request",
            value={
                "name": "Safari Park Hotel",
                "category": "venue",
                "contact_person": "Grace Wanjiru",
                "phone": "+254701234567",
                "email": "grace@safaripark.co.ke",
                "notes": "Reception venue - Garden view. Final quote.",
            },
            request_only=True,
        )
    ],
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
                            "wedding_profile": "aisha.vincent@gmail.com",
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


vendor_search_docs = extend_schema(
    summary="Search wedding vendors",
    description="Search vendors by name, category, or contact person",
    parameters=[
        OpenApiParameter(
            name="q",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Search query (searches in name, category, contact_person)",
            required=True,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Search Results",
                    value={
                        "success": True,
                        "message": "Vendor search completed successfully",
                        "data": [
                            {
                                "id": 1,
                                "wedding_profile": "aisha.vincent@gmail.com",
                                "name": "Nairobi Flowers Ltd",
                                "category": "flowers",
                                "contact_person": "Mary Nyambura",
                                "phone": "+254722123456",
                                "email": "info@nairobiflowers.co.ke",
                                "notes": "Specializes in bridal bouquets",
                                "created_at": "2025-08-26T10:30:00.123456Z",
                                "updated_at": "2025-08-26T10:30:00.123456Z",
                            },
                            {
                                "id": 2,
                                "wedding_profile": "aisha.vincent@gmail.com",
                                "name": "Rose Garden Florists",
                                "category": "flowers",
                                "contact_person": "Fatuma Said",
                                "phone": "+254733987654",
                                "email": "orders@rosegarden.co.ke",
                                "notes": "Beautiful coastal wedding arrangements",
                                "created_at": "2025-08-26T11:15:30.789123Z",
                                "updated_at": "2025-08-26T11:15:30.789123Z",
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


vendor_categories_docs = extend_schema(
    summary="Get vendor categories",
    description="Get list of vendor categories for the wedding",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Categories List",
                    value={
                        "success": True,
                        "message": "Vendor categories retrieved successfully",
                        "data": {
                            "categories": [
                                {
                                    "category": "flowers",
                                    "count": 2,
                                    "vendors": [
                                        "Nairobi Flowers Ltd",
                                        "Rose Garden Florists",
                                    ],
                                },
                                {
                                    "category": "catering",
                                    "count": 1,
                                    "vendors": ["Safari Catering Services"],
                                },
                                {
                                    "category": "photography",
                                    "count": 1,
                                    "vendors": ["Amazing Shots Photography"],
                                },
                                {
                                    "category": "music",
                                    "count": 1,
                                    "vendors": ["DJ Spinmaster Entertainment"],
                                },
                            ],
                            "total_vendors": 5,
                            "total_categories": 4,
                        },
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_VENDOR_ERRORS,
    },
)
