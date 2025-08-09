# Create your tests here.
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_creation() -> None:
    """Test that a user can be created successfully."""
    user = User.objects.create_user(username="testuser", password="testpass123")  # noqa # nosec
    assert user.username == "testuser"  # noqa # nosec
    assert user.check_password("testpass123")  # noqa # nosec
