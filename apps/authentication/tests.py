"""Comprehensive tests for Authentication app."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserSerializer

User = get_user_model()


@pytest.fixture
def api_client():
    """Return API client for testing."""
    return APIClient()


@pytest.fixture
def test_user():
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def auth_client(api_client, test_user):
    """Return authenticated API client."""
    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.mark.django_db
def test_user_creation():
    """Test that a user can be created successfully."""
    user = User.objects.create_user(username="testuser", password="testpass123")
    assert user.username == "testuser"
    assert user.check_password("testpass123")


@pytest.mark.django_db
class TestUserRegistrationSerializer:
    """Test user registration serializer."""

    def test_valid_registration(self):
        """Test valid user registration."""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        serializer = UserRegistrationSerializer(data=data)
        assert serializer.is_valid()

        user = serializer.save()
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.check_password("StrongPass123!")

    def test_password_mismatch(self):
        """Test password confirmation mismatch."""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "StrongPass123!",
            "password_confirm": "differentpass",
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert "Passwords don't match" in str(serializer.errors)

    def test_weak_password(self):
        """Test weak password validation."""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "123",
            "password_confirm": "123",
        }
        serializer = UserRegistrationSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors


@pytest.mark.django_db
class TestUserLoginSerializer:
    """Test user login serializer."""

    def test_valid_login(self, test_user):
        """Test valid login credentials."""
        data = {"username": "testuser", "password": "testpass123"}
        serializer = UserLoginSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["user"] == test_user

    def test_invalid_username(self):
        """Test invalid username."""
        data = {"username": "nonexistent", "password": "testpass123"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "Invalid credentials" in str(serializer.errors)

    def test_invalid_password(self, test_user):
        """Test invalid password."""
        data = {"username": "testuser", "password": "wrongpass"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "Invalid credentials" in str(serializer.errors)

    def test_inactive_user(self):
        """Test login with inactive user."""
        User.objects.create_user(
            username="inactive", password="testpass123", is_active=False
        )
        data = {"username": "inactive", "password": "testpass123"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "User account is disabled" in str(serializer.errors)


@pytest.mark.django_db
class TestUserSerializer:
    """Test user serializer."""

    def test_user_serialization(self, test_user):
        """Test user data serialization."""
        serializer = UserSerializer(test_user)
        data = serializer.data

        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert "password" not in data  # Ensure password is not exposed


@pytest.mark.django_db
class TestAuthenticationViews:
    """Test authentication API endpoints."""

    def test_register_success(self, api_client):
        """Test successful user registration."""
        url = reverse("authentication:register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert "tokens" in response.data["data"]
        assert "user" in response.data["data"]

        # Verify user was created
        user = User.objects.get(username="newuser")
        assert user.email == "new@example.com"

    def test_register_invalid_data(self, api_client):
        """Test registration with invalid data."""
        url = reverse("authentication:register")
        data = {
            "username": "",  # Invalid empty username
            "email": "invalid-email",  # Invalid email format
            "password": "123",  # Weak password
            "password_confirm": "456",  # Password mismatch
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False

    def test_login_success(self, api_client, test_user):
        """Test successful login."""
        url = reverse("authentication:login")
        data = {"username": "testuser", "password": "testpass123"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert "tokens" in response.data["data"]
        assert "user" in response.data["data"]
        assert response.data["data"]["user"]["username"] == "testuser"

    def test_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials."""
        url = reverse("authentication:login")
        data = {"username": "nonexistent", "password": "wrongpass"}
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["success"] is False

    def test_logout_success(self, auth_client, test_user):
        """Test successful logout."""
        refresh = RefreshToken.for_user(test_user)
        url = reverse("authentication:logout")
        data = {"refresh": str(refresh)}

        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert "Logout successful" in response.data["message"]

    def test_logout_invalid_token(self, auth_client):
        """Test logout with invalid refresh token."""
        url = reverse("authentication:logout")
        data = {"refresh": "invalid_token"}

        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False

    def test_profile_get(self, auth_client, test_user):
        """Test getting user profile."""
        url = reverse("authentication:profile")
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["username"] == "testuser"
        assert response.data["data"]["email"] == "test@example.com"

    def test_profile_get_unauthorized(self, api_client):
        """Test getting profile without authentication."""
        url = reverse("authentication:profile")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_profile_update_put(self, auth_client):
        """Test updating profile with PUT."""
        url = reverse("authentication:update_profile")
        data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = auth_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["email"] == "updated@example.com"
        assert response.data["data"]["first_name"] == "Updated"

    def test_profile_update_patch(self, auth_client):
        """Test partial profile update with PATCH."""
        url = reverse("authentication:update_profile")
        data = {"first_name": "PartialUpdate"}

        response = auth_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["data"]["first_name"] == "PartialUpdate"

    def test_profile_update_invalid_data(self, auth_client):
        """Test profile update with invalid data."""
        url = reverse("authentication:update_profile")
        data = {"email": "invalid-email-format"}

        response = auth_client.put(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
