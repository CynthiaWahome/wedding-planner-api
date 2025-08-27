"""Basic validators for Wedding Planner API - Capstone MVP.

Keep it simple for graduation.
"""

import re

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


def validate_kenyan_phone_number(phone_number):
    """Validate Kenyan phone number format."""
    if not phone_number or not phone_number.strip():
        raise ValidationError("Phone number is required.")

    phone_number = phone_number.strip()

    # Remove common formatting characters
    cleaned_number = re.sub(r"[\s\-\(\)]", "", phone_number)

    # Kenyan phone number patterns
    # Format: +254XXXXXXXXX or 254XXXXXXXXX or 0XXXXXXXXX or 7XXXXXXXX/1XXXXXXXX
    kenyan_patterns = [
        r"^\+254[17]\d{8}$",  # +254 followed by 7/1 and 8 digits
        r"^254[17]\d{8}$",  # 254 followed by 7/1 and 8 digits
        r"^0[17]\d{8}$",  # 0 followed by 7/1 and 8 digits
        r"^[17]\d{8}$",  # 7/1 followed by 8 digits
    ]

    if not any(re.match(pattern, cleaned_number) for pattern in kenyan_patterns):
        raise ValidationError(
            "Enter a valid Kenyan phone number "
            "(e.g., +254712345678, 0712345678, or 712345678)."
        )
