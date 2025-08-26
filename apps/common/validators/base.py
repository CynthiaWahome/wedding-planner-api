"""Basic validators for Wedding Planner API - Capstone MVP
Keep it simple for graduation.
.
"""

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_future_date(value):
    """Ensure wedding date is in the future."""
    if value <= timezone.now().date():
        raise ValidationError("Wedding date must be in the future.")


def validate_positive_amount(value):
    """Ensure budget amounts are positive."""
    if value <= 0:
        raise ValidationError("Amount must be greater than zero.")


def validate_guest_count(value):
    """Validate guest count is within acceptable range."""
    if value < 1:
        raise ValidationError("Guest count must be at least 1.")
    if value > 2000:
        raise ValidationError("Guest count cannot exceed 2000.")
