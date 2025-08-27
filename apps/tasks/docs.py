"""OpenAPI documentation for Task Management endpoints - Capstone MVP."""

from drf_spectacular.openapi import OpenApiExample, OpenApiResponse
from drf_spectacular.utils import extend_schema

from apps.common.errors import get_error_documentation
from apps.common.serializers import StandardSuccessResponseSerializer

from .serializers import TaskCreateSerializer

COMMON_TASK_ERRORS = {
    **get_error_documentation(400),
    **get_error_documentation(401),
    **get_error_documentation(403),
    **get_error_documentation(405),
    **get_error_documentation(500),
}


task_list_docs = extend_schema(
    summary="List wedding tasks",
    description="Retrieve all wedding tasks for the authenticated user",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding tasks retrieved successfully",
                        "data": [
                            {
                                "id": 1,
                                "wedding_profile": "aisha.vincent@gmail.com",
                                "title": "Book traditional Pokomo drums",
                                "description": "Find Pokomo drummers for ceremonies!",
                                "assigned_to": "groom",
                                "is_completed": True,
                                "vendor": "Tana River Cultural Group",
                                "created_at": "2025-08-26T16:00:00.123456Z",
                                "updated_at": "2025-08-26T18:30:45.654321Z",
                            },
                            {
                                "id": 2,
                                "wedding_profile": "aisha.vincent@gmail.com",
                                "title": "Design Kamba beadwork accessories",
                                "description": "Commission custom Kamba beadwork",
                                "assigned_to": "bride",
                                "is_completed": False,
                                "vendor": None,
                                "created_at": "2025-08-26T16:15:30.789123Z",
                                "updated_at": "2025-08-26T16:15:30.789123Z",
                            },
                        ],
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_TASK_ERRORS,
    },
)

task_create_docs = extend_schema(
    summary="Create wedding task",
    description="Create a new wedding task for the authenticated user",
    request=TaskCreateSerializer,
    examples=[
        OpenApiExample(
            name="Create Task Request",
            value={
                "title": "Book Marula Studios for Photography",
                "description": "Contact Marula Studios for photography services",
                "assigned_to": "couple",
                "vendor": "Marula Studios",
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
                        "message": "Wedding task created successfully",
                        "data": {
                            "id": 3,
                            "wedding_profile": "grace.njeri@outlook.com",
                            "title": "Book Marula Studios for Photography",
                            "description": "Contact Marula Studios for photography",
                            "assigned_to": "couple",
                            "is_completed": False,
                            "vendor": "Marula Studios",
                            "created_at": "2025-08-26T19:00:15.789123Z",
                            "updated_at": "2025-08-26T19:00:15.789123Z",
                        },
                        "errors": None,
                    },
                )
            ],
        ),
        **COMMON_TASK_ERRORS,
    },
)

task_retrieve_docs = extend_schema(
    summary="Retrieve wedding task",
    description="Get wedding task details by ID",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding task retrieved successfully",
                        "data": {
                            "id": 1,
                            "wedding_profile": "aisha.vincent@gmail.com",
                            "title": "Book Safari Park Hotel for Reception",
                            "description": "Book Safari Park Hotel venue",
                            "assigned_to": "couple",
                            "is_completed": True,
                            "vendor": "Safari Park Hotel",
                            "created_at": "2025-08-26T16:00:00.123456Z",
                            "updated_at": "2025-08-26T18:30:45.654321Z",
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
                        "message": "Wedding task not found",
                        "data": None,
                        "errors": {"detail": "Wedding task not found"},
                    },
                )
            ],
        ),
        **COMMON_TASK_ERRORS,
    },
)

task_update_docs = extend_schema(
    summary="Update wedding task",
    description="Update wedding task details",
    request=TaskCreateSerializer,
    examples=[
        OpenApiExample(
            name="Update Task Request",
            value={
                "title": "Book Safari Park Hotel for Reception & Dinner",
                "description": "Book venue and dinner service",
                "assigned_to": "couple",
                "is_completed": True,
                "vendor": "Safari Park Hotel",
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
                        "message": "Wedding task updated successfully",
                        "data": {
                            "id": 1,
                            "wedding_profile": "aisha.vincent@gmail.com",
                            "title": "Book Safari Park Hotel for Reception & Dinner",
                            "description": "Book venue and dinner service",
                            "assigned_to": "couple",
                            "is_completed": True,
                            "vendor": "Safari Park Hotel",
                            "created_at": "2025-08-26T16:00:00.123456Z",
                            "updated_at": "2025-08-26T20:15:30.987654Z",
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
                        "message": "Wedding task not found",
                        "data": None,
                        "errors": {"detail": "Wedding task not found"},
                    },
                )
            ],
        ),
        **COMMON_TASK_ERRORS,
    },
)

task_delete_docs = extend_schema(
    summary="Delete wedding task",
    description="Delete wedding task by ID",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Success Response",
                    value={
                        "success": True,
                        "message": "Wedding task deleted successfully",
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
                        "message": "Wedding task not found",
                        "data": None,
                        "errors": {"detail": "Wedding task not found"},
                    },
                )
            ],
        ),
        **COMMON_TASK_ERRORS,
    },
)


task_toggle_docs = extend_schema(
    summary="Toggle task completion",
    description="Toggle the completion status of a task",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            examples=[
                OpenApiExample(
                    name="Task Toggled",
                    value={
                        "success": True,
                        "message": "Task completion toggled successfully",
                        "data": {
                            "id": 1,
                            "wedding_profile": "aisha.vincent@gmail.com",
                            "title": "Book traditional Pokomo drums",
                            "description": "Find Pokomo drummers for ceremonies!",
                            "assigned_to": "groom",
                            "is_completed": True,
                            "vendor": "Tana River Cultural Group",
                            "created_at": "2025-08-26T16:00:00.123456Z",
                            "updated_at": "2025-08-26T20:45:30.987654Z",
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
                        "message": "Wedding task not found",
                        "data": None,
                        "errors": {"detail": "Wedding task not found"},
                    },
                )
            ],
        ),
        **COMMON_TASK_ERRORS,
    },
)
