"""Comprehensive tests for Tasks app."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from apps.profiles.models import WeddingProfile
from apps.vendors.models import Vendor

from .models import Task
from .serializers import TaskCreateSerializer, TaskSerializer

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
        user=test_user, wedding_date="2025-06-15", bride_name="Jane Doe", groom_name="John Smith"
    )


@pytest.fixture
def vendor(wedding_profile):
    """Create a test vendor."""
    return Vendor.objects.create(
        wedding_profile=wedding_profile,
        name="Test Vendor",
        category="catering",
        contact_person="Contact Person",
        phone="123-456-7890",
    )


@pytest.fixture
def task(wedding_profile, vendor):
    """Create a test task."""
    return Task.objects.create(
        wedding_profile=wedding_profile,
        title="Test Task",
        description="Test task description",
        assigned_to="bride",
        vendor=vendor,
    )


@pytest.mark.django_db
def test_task_str():
    """Test the string representation of the Task model."""
    user = User.objects.create(username="testuser")
    profile = WeddingProfile.objects.create(
        user=user,
        wedding_date="2025-12-31",
        bride_name="Jane",
        groom_name="John",
        venue="Test Venue",
        budget=10000,
    )
    vendor = Vendor.objects.create(
        wedding_profile=profile,
        name="Cake Boss",
        category="Bakery",
        contact_person="Carlos",
        phone="123456789",
        email="cake@boss.com",
    )
    task = Task.objects.create(
        wedding_profile=profile,
        title="Order Cake",
        description="Order wedding cake from vendor.",
        assigned_to="couple",
        is_completed=False,
        vendor=vendor,
    )
    assert str(task) == "Order Cake"


@pytest.mark.django_db
class TestTaskModel:
    """Test task model functionality."""

    def test_create_task(self, wedding_profile):
        """Test creating a basic task."""
        task = Task.objects.create(
            wedding_profile=wedding_profile,
            title="Choose Wedding Dress",
            description="Visit bridal shops and select dress",
            assigned_to="bride",
        )

        assert task.wedding_profile == wedding_profile
        assert task.title == "Choose Wedding Dress"
        assert task.assigned_to == "bride"
        assert task.is_completed is False

    def test_task_with_vendor(self, wedding_profile, vendor):
        """Test creating task with vendor association."""
        task = Task.objects.create(
            wedding_profile=wedding_profile,
            title="Cake Tasting",
            assigned_to="couple",
            vendor=vendor,
        )

        assert task.vendor == vendor
        assert task.vendor.name == "Test Vendor"


@pytest.mark.django_db
class TestTaskSerializer:
    """Test task serializer."""

    def test_serialize_task(self, task):
        """Test serializing task data."""
        serializer = TaskSerializer(task)
        data = serializer.data

        assert data["title"] == "Test Task"
        assert data["description"] == "Test task description"
        assert data["assigned_to"] == "bride"
        assert data["is_completed"] is False
        assert "wedding_profile" in data
        assert "vendor" in data

    def test_validate_assigned_to_valid(self):
        """Test valid assignment validation."""
        serializer = TaskSerializer()
        valid_choices = ["bride", "groom", "couple"]

        for choice in valid_choices:
            validated = serializer.validate_assigned_to(choice)
            assert validated == choice

    def test_validate_assigned_to_invalid(self):
        """Test invalid assignment validation."""
        serializer = TaskSerializer()

        with pytest.raises(Exception):
            serializer.validate_assigned_to("invalid_choice")


@pytest.mark.django_db
class TestTaskCreateSerializer:
    """Test task creation serializer."""

    def test_valid_task_creation(self, wedding_profile, vendor):
        """Test creating task with valid data."""
        data = {
            "title": "Order Wedding Rings",
            "description": "Visit jeweler and order rings",
            "assigned_to": "couple",
            "vendor": vendor.id,
        }

        request = APIRequestFactory().post("/")
        request.user = wedding_profile.user

        serializer = TaskCreateSerializer(data=data, context={"request": request})

        assert serializer.is_valid()
        task = serializer.save()

        assert task.wedding_profile == wedding_profile
        assert task.title == "Order Wedding Rings"
        assert task.assigned_to == "couple"
        assert task.vendor == vendor

    def test_task_creation_without_vendor(self, wedding_profile):
        """Test creating task without vendor."""
        data = {
            "title": "Send Invitations",
            "description": "Mail wedding invitations",
            "assigned_to": "bride",
        }

        request = APIRequestFactory().post("/")
        request.user = wedding_profile.user

        serializer = TaskCreateSerializer(data=data, context={"request": request})

        assert serializer.is_valid()
        task = serializer.save()

        assert task.title == "Send Invitations"
        assert task.vendor is None
