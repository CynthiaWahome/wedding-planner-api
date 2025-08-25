"""Authentication views for the Wedding Planning API.

Provides JWT-based authentication endpoints for user registration,
login, logout, and profile management.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.responses import APIResponse

from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserSerializer

User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """Register a new user account.

    Creates a new user with JWT tokens for immediate login.

    **Request Body:**
    ```json
    {
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "securepassword123",
        "password_confirm": "securepassword123"
    }
    ```

    **Response:**
    ```json
    {
        "success": true,
        "message": "User registered successfully",
        "data": {
            "user": {...},
            "tokens": {
                "access": "jwt_access_token",
                "refresh": "jwt_refresh_token"
            }
        }
    }
    ```
    """
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

    return APIResponse.error(
        errors=serializer.errors,
        message="Registration failed",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """Authenticate user and return JWT tokens.

    **Request Body:**
    ```json
    {
        "username": "johndoe",
        "password": "securepassword123"
    }
    ```

    **Response:**
    ```json
    {
        "success": true,
        "message": "Login successful",
        "data": {
            "user": {...},
            "tokens": {
                "access": "jwt_access_token",
                "refresh": "jwt_refresh_token"
            }
        }
    }
    ```
    """
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

    return APIResponse.unauthorized(errors=serializer.errors, message="Invalid credentials")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user by blacklisting the refresh token.

    **Request Body:**
    ```json
    {
        "refresh": "jwt_refresh_token"
    }
    ```

    **Response:**
    ```json
    {
        "success": true,
        "message": "Logout successful"
    }
    ```
    """
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        return APIResponse.success(message="Logout successful")
    except Exception:
        return APIResponse.error(
            message="Logout failed - invalid refresh token", status_code=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get current authenticated user's profile information.

    **Headers:**
    ```
    Authorization: Bearer <access_token>
    ```

    **Response:**
    ```json
    {
        "success": true,
        "message": "Profile retrieved successfully",
        "data": {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "date_joined": "2024-08-25T10:30:00Z"
        }
    }
    ```
    """
    serializer = UserSerializer(request.user)
    return APIResponse.success(data=serializer.data, message="Profile retrieved successfully")


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update current user's profile information.

    **Request Body (PUT - all fields required, PATCH - partial update):**
    ```json
    {
        "email": "newemail@example.com",
        "first_name": "UpdatedName",
        "last_name": "UpdatedLastName"
    }
    ```

    **Response:**
    ```json
    {
        "success": true,
        "message": "Profile updated successfully",
        "data": {...}
    }
    ```
    """
    partial = request.method == "PATCH"
    serializer = UserSerializer(request.user, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return APIResponse.success(data=serializer.data, message="Profile updated successfully")

    return APIResponse.error(
        errors=serializer.errors,
        message="Profile update failed",
        status_code=status.HTTP_400_BAD_REQUEST,
    )
