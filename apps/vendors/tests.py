import pytest
from django.contrib.auth import get_user_model

from apps.profiles.models import WeddingProfile
from apps.vendors.models import Vendor

User = get_user_model()


@pytest.mark.django_db
def test_vendor_str() -> None:
    """Test the string representation of the Vendor model."""
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
    assert str(vendor) == "Cake Boss"
