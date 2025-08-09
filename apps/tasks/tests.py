import pytest
from django.contrib.auth import get_user_model

from apps.profiles.models import WeddingProfile
from apps.tasks.models import Task
from apps.vendors.models import Vendor

User = get_user_model()


@pytest.mark.django_db
def test_task_str() -> None:
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
    assert str(task) == "Order Cake"  # noqa
