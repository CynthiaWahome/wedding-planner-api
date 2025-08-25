"""Constants for Wedding Planner API - Capstone MVP
Keep it simple for graduation, expand after.
"""


# Task Assignment (MVP)
class TaskAssignment:
    BRIDE = "bride"
    GROOM = "groom"
    COUPLE = "couple"

    CHOICES = [
        (BRIDE, "Bride"),
        (GROOM, "Groom"),
        (COUPLE, "Couple"),
    ]


# Guest RSVP Status (MVP)
class RSVPStatus:
    INVITED = "invited"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    MAYBE = "maybe"

    CHOICES = [
        (INVITED, "Invited"),
        (CONFIRMED, "Confirmed"),
        (DECLINED, "Declined"),
        (MAYBE, "Maybe"),
    ]


# Basic Vendor Categories (MVP)
class VendorCategory:
    VENUE = "venue"
    CATERING = "catering"
    PHOTOGRAPHY = "photography"
    MUSIC = "music"
    DECORATION = "decoration"
    ATTIRE = "attire"
    OTHER = "other"

    CHOICES = [
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
    BEST_MAN = "best_man"
    BEST_LADY = "best_lady"
    BRIDESMAID = "bridesmaid"
    GROOMSMAN = "groomsman"
    FAMILY = "family"
    COORDINATOR = "coordinator"
    OTHER = "other"

    CHOICES = [
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
