import pytest
from django.contrib.auth import get_user_model

from apps.profiles.models import WeddingProfile

User = get_user_model()


@pytest.mark.django_db
def test_wedding_profile_str() -> None:
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
    assert str(profile) == "Jane & John (2025-12-31)"  # noqa
