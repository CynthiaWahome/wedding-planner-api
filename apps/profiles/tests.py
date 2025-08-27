"""Comprehensive tests for Wedding Profiles app."""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from .models import WeddingProfile
from .serializers import WeddingProfileCreateSerializer, WeddingProfileSerializer

User = get_user_model()


@pytest.fixture
def test_user():
    """Create a test user."""
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def wedding_profile(test_user):
    """Create a test wedding profile."""
    return WeddingProfile.objects.create(
        user=test_user,
        wedding_date=date.today() + timedelta(days=365),
        bride_name="Jane Doe",
        groom_name="Vincent Simiyu",
        venue="Beautiful Garden",
        budget=Decimal("50000.00"),
    )


@pytest.fixture
def api_request_factory():
    """Return API request factory."""
    return APIRequestFactory()


@pytest.mark.django_db
def test_wedding_profile_str():
    """Test the string representation of the WeddingProfile model."""
    user = User.objects.create(username="testuser")
    profile = WeddingProfile.objects.create(
        user=user,
        wedding_date="2025-12-31",
        bride_name="Jane",
        groom_name="John",
        venue="Test Venue",
        budget=10000,
    )
    assert str(profile) == "Jane & John (2025-12-31)"


@pytest.mark.django_db
class TestWeddingProfileModel:
    """Test wedding profile model."""

    def test_create_wedding_profile(self, test_user):
        """Test creating a wedding profile."""
        profile = WeddingProfile.objects.create(
            user=test_user,
            wedding_date=date.today() + timedelta(days=200),
            bride_name="Emma Wilson",
            groom_name="Michael Brown",
            venue="City Hall",
            budget=Decimal("25000.00"),
        )

        assert profile.user == test_user
        assert profile.bride_name == "Emma Wilson"
        assert profile.groom_name == "Michael Brown"
        assert profile.venue == "City Hall"
        assert profile.budget == Decimal("25000.00")

    def test_wedding_profile_optional_fields(self, test_user):
        """Test wedding profile with optional fields."""
        profile = WeddingProfile.objects.create(
            user=test_user,
            wedding_date=date.today() + timedelta(days=150),
            bride_name="Sarah Davis",
            groom_name="James Miller",
            # venue and budget are optional
        )

        assert profile.venue == ""
        assert profile.budget is None


@pytest.mark.django_db
class TestWeddingProfileSerializer:
    """Test wedding profile serializer."""

    def test_serialize_wedding_profile(self, wedding_profile):
        """Test serializing wedding profile data."""
        serializer = WeddingProfileSerializer(wedding_profile)
        data = serializer.data

        assert data["bride_name"] == "Jane Doe"
        assert data["groom_name"] == "Vincent Simiyu"
        assert data["venue"] == "Beautiful Garden"
        assert data["budget"] == "50000.00"
        assert "user" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_validate_wedding_date_future(self):
        """Test wedding date validation for future date."""
        future_date = date.today() + timedelta(days=90)
        serializer = WeddingProfileSerializer()

        # Should not raise any exception
        validated_date = serializer.validate_wedding_date(future_date)
        assert validated_date == future_date

    def test_validate_wedding_date_past(self):
        """Test wedding date validation for past date."""
        past_date = date.today() - timedelta(days=30)
        serializer = WeddingProfileSerializer()

        with pytest.raises(Exception):  # ValidationError will be raised
            serializer.validate_wedding_date(past_date)

    def test_validate_budget_positive(self):
        """Test budget validation for positive amount."""
        positive_amount = Decimal("60000.00")
        serializer = WeddingProfileSerializer()

        # Should not raise any exception
        validated_amount = serializer.validate_budget(positive_amount)
        assert validated_amount == positive_amount

    def test_validate_budget_none(self):
        """Test budget validation for None value."""
        serializer = WeddingProfileSerializer()

        # Should not raise any exception for None
        validated_amount = serializer.validate_budget(None)
        assert validated_amount is None

    def test_validate_budget_negative(self):
        """Test budget validation for negative amount."""
        negative_amount = Decimal("-5000.00")
        serializer = WeddingProfileSerializer()

        with pytest.raises(Exception):  # ValidationError will be raised
            serializer.validate_budget(negative_amount)


@pytest.mark.django_db
class TestWeddingProfileCreateSerializer:
    """Test wedding profile creation serializer."""

    def test_valid_profile_creation_data(self):
        """Test valid profile creation data."""
        data = {
            "wedding_date": date.today() + timedelta(days=180),
            "bride_name": "Lisa Green",
            "groom_name": "Tom White",
            "venue": "Beach Resort",
            "budget": "75000.00",
        }

        serializer = WeddingProfileCreateSerializer(data=data)
        assert serializer.is_valid()

    def test_invalid_past_wedding_date(self):
        """Test invalid past wedding date."""
        data = {
            "wedding_date": date.today() - timedelta(days=30),
            "bride_name": "Anna Blue",
            "groom_name": "Mark Red",
        }

        serializer = WeddingProfileCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "wedding_date" in serializer.errors

    def test_invalid_negative_budget(self):
        """Test invalid negative budget."""
        data = {
            "wedding_date": date.today() + timedelta(days=120),
            "bride_name": "Sophie Black",
            "groom_name": "Chris Gray",
            "budget": "-10000.00",
        }

        serializer = WeddingProfileCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "budget" in serializer.errors

    def test_create_profile_with_user_context(self, test_user, api_request_factory):
        """Test creating profile with user from context."""
        data = {
            "wedding_date": date.today() + timedelta(days=250),
            "bride_name": "Rachel Pink",
            "groom_name": "Daniel Purple",
            "venue": "Mountain Lodge",
        }

        # Mock request with user
        request = api_request_factory.post("/")
        request.user = test_user

        serializer = WeddingProfileCreateSerializer(
            data=data, context={"request": request}
        )

        assert serializer.is_valid()
        profile = serializer.save()

        assert profile.user == test_user
        assert profile.bride_name == "Rachel Pink"
        assert profile.groom_name == "Daniel Purple"
        assert profile.venue == "Mountain Lodge"

    def test_minimal_profile_creation(self, test_user, api_request_factory):
        """Test creating profile with minimal required data."""
        data = {
            "wedding_date": date.today() + timedelta(days=100),
            "bride_name": "Minimal Bride",
            "groom_name": "Minimal Groom",
        }

        request = api_request_factory.post("/")
        request.user = test_user

        serializer = WeddingProfileCreateSerializer(
            data=data, context={"request": request}
        )

        assert serializer.is_valid()
        profile = serializer.save()

        assert profile.user == test_user
        assert profile.bride_name == "Minimal Bride"
        assert profile.groom_name == "Minimal Groom"
        assert profile.venue == ""  # Default empty string
        assert profile.budget is None  # Default None
