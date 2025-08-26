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
    """RSVP status choices for guests."""

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
    """Vendor category choices."""

    VENUE = "venue"
    CATERING = "catering"
    PHOTOGRAPHY = "photography"
    MUSIC = "music"
    DECORATION = "decoration"
    ATTIRE = "attire"
    OTHER = "other"

    CHOICES: ClassVar = [
        (VENUE, "Venue"),
        (CATERING, "Catering"),
        (PHOTOGRAPHY, "Photography"),
        (MUSIC, "Music & Entertainment"),
        (DECORATION, "Decoration"),
        (ATTIRE, "Attire"),
        (OTHER, "Other"),
    ]


# Team Roles (MVP)
class TeamRole:
    """Team role choices for wedding party."""

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
    FORBIDDEN = "Access forbidden"
    VALIDATION_ERROR = "Validation failed"
    INTERNAL_ERROR = "Internal server error"
