"""Cross-app business validation rules.

Contains validation logic that spans multiple apps or represents
core business rules for the wedding planning domain.
"""

from datetime import timedelta

from django.core.exceptions import ValidationError


def validate_guest_count_limit(guest_count, venue_capacity=None):
    """Validate guest count doesn't exceed reasonable limits or venue capacity."""
    if guest_count < 1:
        raise ValidationError("Wedding must have at least 1 guest.")

    if guest_count > 2000:
        raise ValidationError("Guest count cannot exceed 2000 for system limits.")

    if venue_capacity and guest_count > venue_capacity:
        raise ValidationError(
            f"Guest count ({guest_count}) exceeds venue capacity ({venue_capacity})."
        )


def validate_budget_allocation(total_budget, allocated_amount):
    """Validate allocated amount doesn't exceed total budget."""
    if allocated_amount > total_budget:
        raise ValidationError(
            f"Allocated amount ({allocated_amount}) cannot exceed "
            f"total budget ({total_budget})."
        )


def validate_wedding_timeline(wedding_date, event_date, event_name="event"):
    """Validate event dates make sense relative to wedding date."""
    if event_date > wedding_date:
        raise ValidationError(
            f"{event_name} cannot be scheduled after the wedding date."
        )

    two_years_before = wedding_date.replace(year=wedding_date.year - 2)
    if event_date < two_years_before:
        raise ValidationError(
            f"{event_name} cannot be more than 2 years before wedding."
        )


def validate_rsvp_deadline(wedding_date, rsvp_deadline):
    """Validate RSVP deadline is before wedding date."""
    if rsvp_deadline >= wedding_date:
        raise ValidationError("RSVP deadline must be before the wedding date.")

    one_week_before = wedding_date - timedelta(days=7)
    if rsvp_deadline > one_week_before:
        raise ValidationError("RSVP deadline should be at least 1 week before wedding.")


def validate_vendor_service_date(wedding_date, service_date, vendor_type):
    """Validate vendor service date aligns with wedding plans."""
    if service_date != wedding_date:
        days_diff = abs((service_date - wedding_date).days)
        if days_diff > 7:
            raise ValidationError(
                f"{vendor_type} service date is more than 1 week from wedding date."
            )
