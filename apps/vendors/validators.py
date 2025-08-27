"""Vendor management validation functions.

Contains validation logic specific to vendor management, contracts,
and vendor-related information.
"""

import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from apps.common.constants import PaymentTerms, ValidationLimits, VendorCategory
from apps.common.validators.base import (
    validate_kenyan_phone_number,
    validate_positive_amount,
)


def validate_vendor_name(vendor_name):
    """Validate vendor/business name format."""
    if not vendor_name or not vendor_name.strip():
        raise ValidationError("Vendor name is required.")

    vendor_name = vendor_name.strip()

    if len(vendor_name) < 2:
        raise ValidationError("Vendor name must be at least 2 characters long.")

    if len(vendor_name) > 200:
        raise ValidationError("Vendor name cannot exceed 200 characters.")

    if not re.match(r"^[a-zA-Z0-9\s\-'.,&()]+$", vendor_name):
        raise ValidationError(
            "Vendor name can only contain letters, numbers, spaces, "
            "and common punctuation (- ' . , & ( ))."
        )


def validate_vendor_category(category):
    """Validate vendor service category."""
    valid_categories = [
        VendorCategory.CATERING,
        VendorCategory.PHOTOGRAPHY,
        VendorCategory.VIDEOGRAPHY,
        VendorCategory.MUSIC_DJ,
        VendorCategory.LIVE_BAND,
        VendorCategory.FLOWERS,
        VendorCategory.DECORATIONS,
        VendorCategory.VENUE,
        VendorCategory.TRANSPORTATION,
        VendorCategory.BEAUTY,
        VendorCategory.ATTIRE,
        VendorCategory.JEWELRY,
        VendorCategory.STATIONERY,
        VendorCategory.CAKE,
        VendorCategory.PLANNING,
        VendorCategory.OTHER,
    ]

    if category not in valid_categories:
        raise ValidationError(
            f"Vendor category must be one of: {', '.join(valid_categories)}."
        )


def validate_vendor_contact_info(contact_info_type, contact_value):
    """Validate vendor contact information based on type."""
    if contact_value is None or contact_value == "":
        raise ValidationError(f"Vendor {contact_info_type} is required.")

    contact_value = contact_value.strip()

    if contact_info_type == "email":
        try:
            validate_email(contact_value)
        except ValidationError as e:
            raise ValidationError(
                "Please enter a valid email address for the vendor."
            ) from e

    elif contact_info_type == "phone":
        validate_kenyan_phone_number(contact_value)

    elif contact_info_type == "website":
        if not re.match(r"^https?://[^\s]+\.[^\s]+$", contact_value):
            raise ValidationError(
                "Please enter a valid website URL (must start with http:// or https://)."
            )


def validate_vendor_rating(rating):
    """Validate vendor rating value."""
    if rating is None:
        return  # Rating is optional

    if not isinstance(rating, int | float):
        raise ValidationError("Vendor rating must be a number.")

    if rating < 0 or rating > 5:
        raise ValidationError("Vendor rating must be between 0 and 5.")


def validate_service_cost(cost, cost_type="fixed"):
    """Validate vendor service cost."""
    if cost is None:
        return  # Cost is optional (for inquiry stage)

    validate_positive_amount(cost)

    if cost < ValidationLimits.MIN_SERVICE_COST:
        raise ValidationError(
            f"Service cost should be at least KSH "
            f"{ValidationLimits.MIN_SERVICE_COST:,}."
        )

    if cost > ValidationLimits.MAX_SERVICE_COST:
        raise ValidationError(
            f"Service cost cannot exceed KSH {ValidationLimits.MAX_SERVICE_COST:,}."
        )

    if cost_type == "hourly" and cost > ValidationLimits.MAX_HOURLY_RATE:
        raise ValidationError(
            f"Hourly rate cannot exceed KSH {ValidationLimits.MAX_HOURLY_RATE:,} "
            "per hour."
        )


def validate_contract_terms(terms):
    """Validate vendor contract terms content."""
    if terms is None or terms == "":
        return  # Contract terms are optional

    terms = terms.strip()

    if len(terms) < 20:
        raise ValidationError(
            "Contract terms should be at least 20 characters if provided."
        )

    if len(terms) > 5000:
        raise ValidationError("Contract terms cannot exceed 5000 characters.")

    suspicious_patterns = ["<script", "javascript:", "data:"]
    for pattern in suspicious_patterns:
        if pattern.lower() in terms.lower():
            raise ValidationError("Contract terms contain invalid content.")


def validate_vendor_availability_date(availability_date, wedding_date=None):
    """Validate vendor availability date."""
    if availability_date is None:
        return  # Availability date is optional

    from datetime import timedelta

    from django.utils import timezone

    today = timezone.now().date()

    if availability_date < today:
        raise ValidationError("Vendor availability date cannot be in the past.")

    if wedding_date:
        max_range = wedding_date + timedelta(days=30)
        min_range = wedding_date - timedelta(days=30)

        if availability_date > max_range or availability_date < min_range:
            raise ValidationError(
                "Vendor availability should be within 30 days of the wedding date."
            )


def validate_vendor_service_description(description):
    """Validate vendor service description."""
    if description is None or description == "":
        return  # Service description is optional

    description = description.strip()

    if len(description) < 10:
        raise ValidationError(
            "Service description should be at least 10 characters if provided."
        )

    if len(description) > 2000:
        raise ValidationError("Service description cannot exceed 2000 characters.")

    suspicious_patterns = ["<script", "javascript:", "data:"]
    for pattern in suspicious_patterns:
        if pattern.lower() in description.lower():
            raise ValidationError("Service description contains invalid content.")


def validate_vendor_payment_terms(payment_terms):
    """Validate vendor payment terms."""
    valid_terms = [
        PaymentTerms.FULL_UPFRONT,
        PaymentTerms.DEPOSIT_50,
        PaymentTerms.DEPOSIT_30,
        PaymentTerms.INSTALLMENTS,
        PaymentTerms.PAYMENT_ON_DELIVERY,
        PaymentTerms.NET_30,
        PaymentTerms.CUSTOM,
    ]

    if payment_terms not in valid_terms:
        raise ValidationError(
            f"Payment terms must be one of: {', '.join(valid_terms)}."
        )
