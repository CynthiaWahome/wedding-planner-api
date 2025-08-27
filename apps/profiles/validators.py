"""Wedding Profile validation functions.

Contains validation logic specific to wedding profiles, budgets,
venues, and wedding-related information.
"""

import re
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.common.constants import ValidationLimits
from apps.common.validators.base import validate_future_date, validate_positive_amount


def validate_wedding_date_range(wedding_date):
    """Validate wedding date is reasonable for planning purposes."""
    validate_future_date(wedding_date)

    today = timezone.now().date()
    max_future = today + timedelta(days=365 * 5)

    if wedding_date > max_future:
        raise ValidationError("Wedding date cannot be more than 5 years in the future.")

    min_planning_date = today + timedelta(days=30)
    if wedding_date < min_planning_date:
        raise ValidationError(
            "Wedding date should be at least 1 month in the future for proper planning."
        )


def validate_wedding_budget_structure(budget):
    """Validate wedding budget meets reasonable expectations."""
    if budget is None:
        return

    validate_positive_amount(budget)

    if budget < ValidationLimits.MIN_BUDGET:
        raise ValidationError(
            f"Wedding budget should be at least KSH {ValidationLimits.MIN_BUDGET:,} "
            "for a basic wedding."
        )

    if budget > ValidationLimits.MAX_BUDGET:
        raise ValidationError(
            f"Wedding budget cannot exceed KSH {ValidationLimits.MAX_BUDGET:,} "
            "for system limits."
        )


def validate_venue_name(venue_name):
    """Validate venue name format and content."""
    if not venue_name or not venue_name.strip():
        raise ValidationError("Venue name is required.")

    venue_name = venue_name.strip()

    if len(venue_name) < 3:
        raise ValidationError("Venue name must be at least 3 characters long.")

    if len(venue_name) > 200:
        raise ValidationError("Venue name cannot exceed 200 characters.")

    if not re.match(r"^[a-zA-Z0-9\s\-'.,&()]+$", venue_name):
        raise ValidationError(
            "Venue name can only contain letters, numbers, spaces, "
            "and common punctuation (- ' . , & ( ))."
        )


def validate_bride_groom_names(bride_name, groom_name):
    """Validate bride and groom names together for wedding consistency."""
    if not bride_name or not bride_name.strip():
        raise ValidationError("Bride name is required.")

    if not groom_name or not groom_name.strip():
        raise ValidationError("Groom name is required.")

    _validate_person_name(bride_name.strip(), "Bride")
    _validate_person_name(groom_name.strip(), "Groom")

    if bride_name.strip().lower() == groom_name.strip().lower():
        raise ValidationError("Bride and groom names cannot be the same.")


def _validate_person_name(name, person_type):
    """Internal helper to validate individual person names."""
    if len(name) < 2:
        raise ValidationError(f"{person_type} name must be at least 2 characters long.")

    if len(name) > 100:
        raise ValidationError(f"{person_type} name cannot exceed 100 characters.")

    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        raise ValidationError(
            f"{person_type} name can only contain letters, spaces, "
            "hyphens, and apostrophes."
        )

    if name.count(" ") > 4:
        raise ValidationError(f"{person_type} name cannot have more than 4 spaces.")


def validate_wedding_description(description):
    """Validate wedding description content and length."""
    if description is None or description == "":
        return

    description = description.strip()

    if len(description) < 10:
        raise ValidationError(
            "Wedding description should be at least 10 characters if provided."
        )

    if len(description) > 1000:
        raise ValidationError("Wedding description cannot exceed 1000 characters.")

    suspicious_patterns = ["<script", "javascript:", "data:"]
    for pattern in suspicious_patterns:
        if pattern.lower() in description.lower():
            raise ValidationError("Wedding description contains invalid content.")


def validate_guest_count_for_venue(guest_count, venue_capacity=None):
    """Validate guest count makes sense for the venue."""
    if guest_count is None:
        return

    if guest_count < 1:
        raise ValidationError("Guest count must be at least 1.")

    if guest_count > 2000:
        raise ValidationError("Guest count cannot exceed 2000 for system limitations.")

    if venue_capacity and guest_count > venue_capacity:
        raise ValidationError(
            f"Guest count ({guest_count}) exceeds venue capacity ({venue_capacity})."
        )
