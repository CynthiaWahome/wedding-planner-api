"""OpenAPI documentation for Guest Management endpoints - Capstone MVP."""

from drf_spectacular.openapi import OpenApiExample, OpenApiResponse
from drf_spectacular.utils import extend_schema

from apps.common.errors import get_error_documentation
from apps.common.serializers import StandardSuccessResponseSerializer

from .serializers import GuestSerializer, RSVPUpdateSerializer

COMMON_GUEST_ERRORS = {
    **get_error_documentation(400),
    **get_error_documentation(401),
    **get_error_documentation(403),
    **get_error_documentation(405),
    **get_error_documentation(500),
}


guest_list_docs = extend_schema(
    summary="List wedding guests",
    description="Retrieve all wedding guests for the authenticated user",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding guests retrieved successfully",
                        "data": [
                            {
                                "id": 1,
                                "wedding_profile": "aisha.vincent@gmail.com",
                                "name": "Khadija Ali",
                                "email": "khadija.ali@gmail.com",
                                "rsvp_status": "confirmed",
                                "plus_one": True,
                                "created_at": "2025-08-26T12:00:00.123456Z",
                                "updated_at": "2025-08-26T16:30:45.654321Z",
                            },
                            {
                                "id": 2,
                                "wedding_profile": "aisha.vincent@gmail.com",
                                "name": "Kiprotich Cheruiyot",
                                "email": "kiprotich.cheruiyot@yahoo.com",
                                "rsvp_status": "invited",
                                "plus_one": False,
                                "created_at": "2025-08-26T12:15:30.789123Z",
                                "updated_at": "2025-08-26T12:15:30.789123Z",
                            },
                        ],
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_GUEST_ERRORS,
    },
)

guest_create_docs = extend_schema(
    summary="Create wedding guest",
    description="Add a new guest to the wedding guest list",
    request=GuestSerializer,
    examples=[
        OpenApiExample(
            name="Create Guest Request",
            value={
                "name": "Lomuria Lokol",
                "email": "lomuria.lokol@gmail.com",
                "rsvp_status": "invited",
                "plus_one": True,
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
                        "message": "Wedding guest created successfully",
                        "data": {
                            "id": 3,
                            "wedding_profile": "grace.njeri@outlook.com",
                            "name": "Catherine Muthoni",
                            "email": "catherine.muthoni@outlook.com",
                            "rsvp_status": "invited",
                            "plus_one": True,
                            "created_at": "2025-08-26T18:00:15.789123Z",
                            "updated_at": "2025-08-26T18:00:15.789123Z",
                        },
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_GUEST_ERRORS,
    },
)

guest_retrieve_docs = extend_schema(
    summary="Retrieve wedding guest",
    description="Get wedding guest details by ID",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding guest retrieved successfully",
                        "data": {
                            "id": 1,
                            "wedding_profile": "aisha.vincent@gmail.com",
                            "name": "Mary Wanjiku",
                            "email": "mary.wanjiku@gmail.com",
                            "rsvp_status": "confirmed",
                            "plus_one": True,
                            "created_at": "2025-08-26T12:00:00.123456Z",
                            "updated_at": "2025-08-26T16:30:45.654321Z",
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
                        "message": "Wedding guest not found",
                        "data": None,
                        "errors": {"detail": "Wedding guest not found"},
                    },
                )
            ],
        ),
        **COMMON_GUEST_ERRORS,
    },
)

guest_update_docs = extend_schema(
    summary="Update wedding guest",
    description="Update wedding guest details",
    request=GuestSerializer,
    examples=[
        OpenApiExample(
            name="Update Guest Request",
            value={
                "name": "Khadija Ali",
                "email": "khadija.ali.updated@gmail.com",
                "rsvp_status": "confirmed",
                "plus_one": False,
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
                        "message": "Wedding guest updated successfully",
                        "data": {
                            "id": 1,
                            "wedding_profile": "aisha.vincent@gmail.com",
                            "name": "Mary Wanjiku",
                            "email": "mary.wanjiku.new@gmail.com",
                            "rsvp_status": "confirmed",
                            "plus_one": False,
                            "created_at": "2025-08-26T12:00:00.123456Z",
                            "updated_at": "2025-08-26T18:45:30.987654Z",
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
                        "message": "Wedding guest not found",
                        "data": None,
                        "errors": {"detail": "Wedding guest not found"},
                    },
                )
            ],
        ),
        **COMMON_GUEST_ERRORS,
    },
)

guest_delete_docs = extend_schema(
    summary="Delete wedding guest",
    description="Delete wedding guest by ID",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding guest deleted successfully",
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
                        "message": "Wedding guest not found",
                        "data": None,
                        "errors": {"detail": "Wedding guest not found"},
                    },
                )
            ],
        ),
        **COMMON_GUEST_ERRORS,
    },
)


guest_rsvp_update_docs = extend_schema(
    summary="Update guest RSVP status",
    description="Update a specific guest's RSVP status",
    request=RSVPUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="RSVP Updated",
                    value={
                        "success": True,
                        "message": "RSVP status updated successfully",
                        "data": {
                            "id": 1,
                            "name": "Maryam Sheikh",
                            "rsvp_status": "confirmed",
                            "updated_at": "2024-08-25T12:30:00Z",
                        },
                    },
                )
            ],
        ),
        **COMMON_GUEST_ERRORS,
    },
)


guest_statistics_docs = extend_schema(
    summary="Get guest statistics",
    description="Retrieve wedding guest statistics and metrics",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Guest Statistics",
                    value={
                        "success": True,
                        "message": "Guest statistics retrieved successfully",
                        "data": {
                            "total_guests": 150,
                            "confirmed": 120,
                            "declined": 15,
                            "pending": 10,
                            "maybe": 5,
                            "plus_ones": 45,
                            "confirmation_rate": 80.0,
                        },
                    },
                )
            ],
        ),
        **COMMON_GUEST_ERRORS,
    },
)
