import pytest
from django.contrib.auth import get_user_model

from apps.guests.models import Guest
from apps.profiles.models import WeddingProfile

User = get_user_model()


@pytest.mark.django_db
def test_guest_str() -> None:
    """Test the string representation of the Guest model."""
    user = User.objects.create(username="testuser")
    profile = WeddingProfile.objects.create(
        user=user,
        wedding_date="2025-12-31",
        bride_name="Jane",
        groom_name="John",
        venue="Test Venue",
        budget=10000,
    )
    guest = Guest.objects.create(
        wedding_profile=profile,
        name="Alice",
        email="alice@example.com",
        rsvp_status="invited",
        plus_one=True,
    )
    assert str(guest) == "Alice (invited)"  # noqa
