"""Guest management validation functions.

Contains validation logic specific to guest management, RSVP handling,
and guest-related information.
"""

import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.common.validators.base import validate_kenyan_phone_number


def validate_guest_name(name):
    """Validate guest name format for Kenyan naming conventions."""
    if not name or not name.strip():
        raise ValidationError("Guest name is required.")

    name = name.strip()

    if len(name) < 2:
        raise ValidationError("Guest name must be at least 2 characters long.")

    if len(name) > 100:
        raise ValidationError("Guest name cannot exceed 100 characters.")

    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        raise ValidationError(
            "Guest name can only contain letters, spaces, hyphens, and apostrophes."
        )

    if name.count(" ") > 4:
        raise ValidationError("Guest name cannot have more than 4 spaces.")


def validate_guest_email_format(email):
    """Validate guest email format if provided."""
    if email is None or email == "":
        return

    email = email.strip()

    try:
        validate_email(email)
    except ValidationError as e:
        raise ValidationError(
            "Please enter a valid email address for the guest."
        ) from e


def validate_rsvp_status(status):
    """Validate RSVP status is one of the allowed choices."""
    from apps.common.constants import ValidationChoices

    if status not in ValidationChoices.RSVP_STATUSES:
        raise ValidationError(
            f"RSVP status must be one of: {', '.join(ValidationChoices.RSVP_STATUSES)}."
        )


def validate_dietary_restrictions(restrictions):
    """Validate dietary restrictions content."""
    if restrictions is None or restrictions == "":
        return

    restrictions = restrictions.strip()

    if len(restrictions) > 500:
        raise ValidationError("Dietary restrictions cannot exceed 500 characters.")

    suspicious_patterns = ["<script", "javascript:", "data:"]
    for pattern in suspicious_patterns:
        if pattern.lower() in restrictions.lower():
            raise ValidationError("Dietary restrictions contain invalid content.")


def validate_guest_contact_info(phone_number):
    """Validate guest contact information."""
    if phone_number is None or phone_number == "":
        return

    validate_kenyan_phone_number(phone_number)


def validate_plus_one_eligibility(guest_type, plus_one_allowed):
    """Validate plus-one eligibility based on guest type."""
    from apps.common.constants import ValidationChoices

    if guest_type in ValidationChoices.RESTRICTED_GUEST_TYPES and plus_one_allowed:
        raise ValidationError(
            f"Guests of type '{guest_type}' cannot have plus-one privileges."
        )


def validate_guest_table_assignment(table_number, max_tables=50):
    """Validate guest table assignment."""
    if table_number is None:
        return

    if table_number < 1:
        raise ValidationError("Table number must be at least 1.")

    if table_number > max_tables:
        raise ValidationError(f"Table number cannot exceed {max_tables}.")


def validate_guest_age_category(age_category):
    """Validate guest age category."""
    from apps.common.constants import ValidationChoices

    if age_category not in ValidationChoices.AGE_CATEGORIES:
        choices_str = ", ".join(ValidationChoices.AGE_CATEGORIES)
        raise ValidationError(f"Age category must be one of: {choices_str}.")
