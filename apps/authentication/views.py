"""Authentication views for the Wedding Planning API.

Provides JWT-based authentication endpoints for user registration,
login, logout, and profile management.
"""

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView

from apps.common.errors import StandardErrors
from apps.common.responses import APIResponse

from .docs import (
    login_docs,
    logout_docs,
    profile_get_docs,
    profile_update_docs,
    register_docs,
    token_refresh_docs,
)
from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserSerializer

User = get_user_model()


@register_docs
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """Register a new user account with JWT tokens for immediate login."""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generate JWT tokens for immediate login
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return APIResponse.created(
            data={
                "user": UserSerializer(user).data,
                "tokens": {"access": str(access_token), "refresh": str(refresh)},
            },
            message="User registered successfully",
        )

    return StandardErrors.bad_request(
        message="Registration failed - please check your input"
    )


@login_docs
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Authenticate user and return JWT tokens."""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return APIResponse.success(
            data={
                "user": UserSerializer(user).data,
                "tokens": {"access": str(access_token), "refresh": str(refresh)},
            },
            message="Login successful",
        )

    return StandardErrors.unauthorized(message="Invalid credentials")


@logout_docs
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user by blacklisting the refresh token."""
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return StandardErrors.bad_request(message="Refresh token required")

        token = RefreshToken(refresh_token)
        token.blacklist()
        return APIResponse.success(message="Logout successful")
    except Exception:
        return StandardErrors.bad_request(
            message="Logout failed - invalid refresh token"
        )


@profile_get_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get current authenticated user's profile information."""
    serializer = UserSerializer(request.user)
    return APIResponse.success(
        data=serializer.data, message="Profile retrieved successfully"
    )


@profile_update_docs
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def update_profile(request):
    """Update current user's profile with atomic transaction support."""
    partial = request.method == "PATCH"
    serializer = UserSerializer(request.user, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return APIResponse.success(
            data=serializer.data, message="Profile updated successfully"
        )

    return StandardErrors.bad_request(
        message="Profile update failed - please check your input"
    )


class TokenRefreshView(BaseTokenRefreshView):
    """Custom token refresh view that matches our standardized API response format."""

    @token_refresh_docs
    def post(self, request, *args, **kwargs):
        """Refresh JWT token and return in standardized format."""
        serializer = TokenRefreshSerializer(data=request.data)

        if serializer.is_valid():
            return APIResponse.success(
                data={
                    "tokens": {
                        "access": serializer.validated_data["access"],
                        "refresh": serializer.validated_data.get("refresh"),
                    }
                },
                message="Token refreshed successfully",
            )

        return StandardErrors.bad_request(
            message="Token refresh failed", errors=list(serializer.errors.values())
        )
