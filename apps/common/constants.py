"""Constants for Wedding Planner API - Capstone MVP.

Keep it simple for graduation, expand after.
"""

from typing import ClassVar


# Task Assignment (MVP)
class TaskAssignment:
    """Task assignment choices for wedding planning."""

    BRIDE = "bride"
    GROOM = "groom"
    COUPLE = "couple"

    CHOICES: ClassVar = [
        (BRIDE, "Bride"),
        (GROOM, "Groom"),
        (COUPLE, "Couple"),
    ]


# Guest RSVP Status (MVP)
class RSVPStatus:
    """RSVP status choices for guest management."""

    INVITED = "invited"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    MAYBE = "maybe"

    CHOICES: ClassVar = [
        (INVITED, "Invited"),
        (CONFIRMED, "Confirmed"),
        (DECLINED, "Declined"),
        (MAYBE, "Maybe"),
    ]


# Basic Vendor Categories (MVP)
class VendorCategory:
    """Vendor category choices for wedding services."""

    CATERING = "catering"
    PHOTOGRAPHY = "photography"
    VIDEOGRAPHY = "videography"
    MUSIC_DJ = "music_dj"
    LIVE_BAND = "live_band"
    FLOWERS = "flowers"
    DECORATIONS = "decorations"
    VENUE = "venue"
    TRANSPORTATION = "transportation"
    BEAUTY = "beauty"
    ATTIRE = "attire"
    JEWELRY = "jewelry"
    STATIONERY = "stationery"
    CAKE = "cake"
    PLANNING = "planning"
    OTHER = "other"

    CHOICES: ClassVar = [
        (CATERING, "Catering"),
        (PHOTOGRAPHY, "Photography"),
        (VIDEOGRAPHY, "Videography"),
        (MUSIC_DJ, "Music DJ"),
        (LIVE_BAND, "Live Band"),
        (FLOWERS, "Flowers"),
        (DECORATIONS, "Decorations"),
        (VENUE, "Venue"),
        (TRANSPORTATION, "Transportation"),
        (BEAUTY, "Beauty"),
        (ATTIRE, "Attire"),
        (JEWELRY, "Jewelry"),
        (STATIONERY, "Stationery"),
        (CAKE, "Cake"),
        (PLANNING, "Planning"),
        (OTHER, "Other"),
    ]


# Team Roles (MVP)
class TeamRole:
    """Team role choices for wedding party members."""

    BEST_MAN = "best_man"
    BEST_LADY = "best_lady"
    BRIDESMAID = "bridesmaid"
    GROOMSMAN = "groomsman"
    FAMILY = "family"
    COORDINATOR = "coordinator"
    OTHER = "other"

    CHOICES: ClassVar = [
        (BEST_MAN, "Best Man"),
        (BEST_LADY, "Best Lady"),
        (BRIDESMAID, "Bridesmaid"),
        (GROOMSMAN, "Groomsman"),
        (FAMILY, "Family Member"),
        (COORDINATOR, "Coordinator"),
        (OTHER, "Other"),
    ]


# Validation Limits
class ValidationLimits:
    """Validation limits for various fields."""

    # Budget limits (KSH)
    MIN_BUDGET = 50000  # KSH 50,000 minimum
    MAX_BUDGET = 50000000  # KSH 50M maximum

    # Service cost limits (KSH)
    MIN_SERVICE_COST = 1000  # KSH 1,000 minimum
    MAX_SERVICE_COST = 10000000  # KSH 10M maximum
    MAX_HOURLY_RATE = 100000  # KSH 100k/hour max

    # Time limits (hours)
    MIN_ESTIMATED_HOURS = 0.25  # 15 minutes minimum
    MAX_ESTIMATED_HOURS = 200  # 200 hours maximum per task


# Payment Terms
class PaymentTerms:
    """Payment terms choices for vendors."""

    FULL_UPFRONT = "full_upfront"
    DEPOSIT_50 = "deposit_50"
    DEPOSIT_30 = "deposit_30"
    INSTALLMENTS = "installments"
    PAYMENT_ON_DELIVERY = "payment_on_delivery"
    NET_30 = "net_30"
    CUSTOM = "custom"

    CHOICES: ClassVar = [
        (FULL_UPFRONT, "Full Upfront"),
        (DEPOSIT_50, "50% Deposit"),
        (DEPOSIT_30, "30% Deposit"),
        (INSTALLMENTS, "Installments"),
        (PAYMENT_ON_DELIVERY, "Payment on Delivery"),
        (NET_30, "Net 30"),
        (CUSTOM, "Custom"),
    ]


# API Response Messages
class Messages:
    """Standard API response messages."""

    # Success
    SUCCESS = "Operation completed successfully"
    CREATED = "Resource created successfully"
    UPDATED = "Resource updated successfully"
    DELETED = "Resource deleted successfully"

    # Errors
    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = "Unauthorized access"
    BAD_REQUEST = "Bad request"
    VALIDATION_ERROR = "Validation error"
