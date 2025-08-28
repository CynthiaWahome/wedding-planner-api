"""Authentication API documentation with DRY error responses."""

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_serializer,
)
from rest_framework import serializers

from apps.common.errors import (
    COMMON_AUTH_ERRORS,
    COMMON_CREATE_ERRORS,
    COMMON_CRUD_ERRORS,
)
from apps.common.serializers import StandardSuccessResponseSerializer

from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserSerializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "User Data Example",
            summary="Grace Njeri Profile",
            description="Example user profile data",
            value={
                "id": 3,
                "username": "grace_njeri",
                "email": "grace.njeri@gmail.com",
                "first_name": "Grace",
                "last_name": "Njeri",
                "date_joined": "2024-08-15T09:45:00Z",
            },
        )
    ]
)
class UserResponseDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="User ID")
    username = serializers.CharField(help_text="Username")
    email = serializers.EmailField(help_text="Email address")
    first_name = serializers.CharField(help_text="First name")
    last_name = serializers.CharField(help_text="Last name")
    date_joined = serializers.DateTimeField(help_text="Date joined")


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "JWT Tokens Example",
            summary="Authentication Tokens",
            description="JWT access and refresh tokens",
            value={
                "access": "eyJhbGciOiJIUzI1NiJ9...access_token",
                "refresh": "eyJhbGciOiJIUzI1NiJ9...refresh_token",
            },
        )
    ]
)
class TokensSerializer(serializers.Serializer):
    access = serializers.CharField(help_text="JWT access token")
    refresh = serializers.CharField(help_text="JWT refresh token")


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Profile Update Success",
            summary="Grace's Profile Updated",
            description="Successfully updated user profile",
            value={
                "success": True,
                "message": "Profile updated successfully",
                "data": {
                    "id": 3,
                    "username": "grace_njeri",
                    "email": "grace.wanjiku@gmail.com",
                    "first_name": "Grace",
                    "last_name": "Wanjiku",
                    "date_joined": "2024-08-15T09:45:00Z",
                },
            },
        )
    ]
)
class LogoutRequestSerializer(serializers.Serializer):
    """Simple logout request serializer for docs."""

    refresh = serializers.CharField(help_text="JWT refresh token to blacklist")

    class Meta:
        """Meta configuration for logout request."""

        swagger_schema_fields = {
            "example": {"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example"}
        }


class TokenRefreshRequestSerializer(serializers.Serializer):
    """Token refresh request serializer for docs."""

    refresh = serializers.CharField(help_text="JWT refresh token")

    class Meta:
        """Meta configuration for token refresh request."""

        swagger_schema_fields = {
            "example": {"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example"}
        }


class TokenRefreshResponseSerializer(serializers.Serializer):
    """Token refresh response serializer for docs."""

    access = serializers.CharField(help_text="New JWT access token")

    class Meta:
        """Meta configuration for token refresh response."""

        swagger_schema_fields = {
            "example": {"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example"}
        }


register_docs = extend_schema(
    tags=["authentication"],
    summary="User Registration",
    description="Register a new user account for wedding planning",
    request=UserRegistrationSerializer,
    responses={
        201: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            description="User registered successfully",
            examples=[
                OpenApiExample(
                    "Registration Success",
                    summary="User Registration Success",
                    value={
                        "success": True,
                        "message": "User registered successfully",
                        "data": {
                            "user": {
                                "id": 1,
                                "username": "wambui_kariuki",
                                "email": "wambui_kariuki@example.com",
                                "first_name": "Wambui",
                                "last_name": "Kariuki",
                                "date_joined": "2024-08-26T10:30:00Z",
                            },
                            "tokens": {
                                "access": "eyJhbGciOiJIUzI1NiJ9...wanjiku_access",
                                "refresh": "eyJhbGciOiJIUzI1NiJ9...wanjiku_refresh",
                            },
                        },
                    },
                )
            ],
        ),
        **COMMON_CREATE_ERRORS,
    },
    examples=[
        OpenApiExample(
            "Registration Request",
            summary="User registration",
            description="Example registration",
            value={
                "username": "wambui_kariuki",
                "email": "wambui_kariukir@example.com",
                "first_name": "Wanjiku",
                "last_name": "Kamau",
                "password": "SecurePass123!",
                "password_confirm": "SecurePass123!",
            },
            request_only=True,
        )
    ],
)

login_docs = extend_schema(
    tags=["authentication"],
    summary="User Login",
    description="Authenticate user and receive JWT tokens",
    request=UserLoginSerializer,
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            description="Login successful",
            examples=[
                OpenApiExample(
                    "Login Success",
                    summary="User Login Success",
                    value={
                        "success": True,
                        "message": "Login successful",
                        "data": {
                            "user": {
                                "id": 2,
                                "username": "vincent_simiyu",
                                "email": "vincent_simiyu@yahoo.com",
                                "first_name": "Vincent",
                                "last_name": "Simiyu",
                                "date_joined": "2024-08-20T14:20:00Z",
                            },
                            "tokens": {
                                "access": "eyJhbGciOiJIUzI1NiJ9...james_access",
                                "refresh": "eyJhbGciOiJIUzI1NiJ9...james_refresh",
                            },
                        },
                    },
                )
            ],
        ),
        **COMMON_AUTH_ERRORS,
    },
    examples=[
        OpenApiExample(
            "Login Request",
            summary="User login with credentials",
            value={"username": "vincent_simiyu", "password": "MyPassword123!"},
            request_only=True,
        )
    ],
)

profile_update_docs = extend_schema(
    tags=["authentication"],
    summary="Update User Profile",
    description="Update authenticated user profile with atomic transactions.",
    request=UserSerializer,
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            description="Profile updated successfully",
            examples=[
                OpenApiExample(
                    "Profile Updated",
                    summary="Grace's profile updated to married name",
                    description="User successfully updated profile information",
                    value={
                        "success": True,
                        "message": "Profile updated successfully",
                        "data": {
                            "id": 3,
                            "username": "grace_njeri",
                            "email": "grace.wanjiku@gmail.com",
                            "first_name": "Grace",
                            "last_name": "Wanjiku",
                            "date_joined": "2024-08-15T09:45:00Z",
                        },
                    },
                )
            ],
        ),
        **COMMON_CRUD_ERRORS,
    },
    examples=[
        OpenApiExample(
            "Profile Update Request",
            summary="Grace updates to married name",
            description="Example showing partial profile update with new married name",
            value={
                "email": "grace.wanjiku@gmail.com",
                "first_name": "Grace",
                "last_name": "Wanjiku",
            },
            request_only=True,
        )
    ],
)

profile_get_docs = extend_schema(
    tags=["authentication"],
    summary="Get User Profile",
    description="Retrieve current authenticated user's profile information",
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            description="Profile retrieved successfully",
            examples=[
                OpenApiExample(
                    "Profile Retrieved",
                    summary="Grace Njeri's profile information",
                    value={
                        "success": True,
                        "message": "Profile retrieved successfully",
                        "data": {
                            "id": 3,
                            "username": "grace_njeri",
                            "email": "grace.njeri@gmail.com",
                            "first_name": "Grace",
                            "last_name": "Njeri",
                            "date_joined": "2024-08-15T09:45:00Z",
                        },
                    },
                )
            ],
        ),
        **COMMON_AUTH_ERRORS,
    },
)

logout_docs = extend_schema(
    tags=["authentication"],
    summary="User Logout",
    description="Logout user by blacklisting refresh token to prevent reuse",
    request=LogoutRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            description="Logout successful",
            examples=[
                OpenApiExample(
                    "Logout Success",
                    summary="User successfully logged out",
                    value={
                        "success": True,
                        "message": "Logout successful",
                        "data": None,
                    },
                )
            ],
        ),
        **COMMON_AUTH_ERRORS,
    },
    examples=[
        OpenApiExample(
            "Logout Request",
            summary="Blacklist refresh token for Grace",
            description="Provide refresh token to logout user gracefully",
            value={"refresh": "eyJhbGciOiJIUzI1NiJ9...grace_logout"},
            request_only=True,
        )
    ],
)

token_refresh_docs = extend_schema(
    tags=["authentication"],
    summary="Refresh JWT Token",
    description="Takes a refresh token and returns a new access token",
    request=LogoutRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=StandardSuccessResponseSerializer,
            description="Token refreshed successfully",
            examples=[
                OpenApiExample(
                    "Token Refresh Success",
                    summary="User token refreshed",
                    value={
                        "success": True,
                        "message": "Token refreshed successfully",
                        "data": {
                            "tokens": {
                                "access": "eyJhbGciOiJIUzI1NiJ9...new_james_access",
                                "refresh": "eyJhbGciOiJIUzI1NiJ9...new_james_refresh",
                            }
                        },
                    },
                )
            ],
        ),
        **COMMON_AUTH_ERRORS,
    },
    examples=[
        OpenApiExample(
            "Token Refresh Request",
            summary="Refresh user access token",
            description="Provide existing refresh token to get new access token",
            value={"refresh": "eyJhbGciOiJIUzI1NiJ9...james_refresh"},
            request_only=True,
        )
    ],
)
