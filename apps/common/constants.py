"""Constants for Wedding Planner API.

Includes:
- TaskAssignment: Choices for assigning wedding planning tasks (Bride, Groom, Couple).
- RSVPStatus: Guest RSVP status options (Invited, Confirmed, Declined, Maybe).
- VendorCategory: Categories for wedding vendors (Venue, Catering, Photography, etc.).
- TeamRole: Roles for wedding party members (Best Man, Bridesmaid, Coordinator, etc.).
- PaymentTerms: Payment options for vendor contracts
  (Full Upfront, Deposit, Installments, etc.).
- ValidationLimits: Limits for budgets, service costs, and estimated hours.
- Messages: Standard API response messages (Success, Error, etc.).
- WeddingProgressDefaults: Default values and thresholds for wedding planning
  progress and budget spending.
- TaskCategory: Categories for planning tasks (Venue, Catering, Invitations, etc.).

"""

from typing import ClassVar


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

    VALID_CHOICES: ClassVar = [
        VENUE,
        CATERING,
        PHOTOGRAPHY,
        MUSIC_DJ,
        DECORATIONS,
        ATTIRE,
        OTHER,
    ]


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


class PaymentTerms:
    """Payment terms choices for vendor contracts."""

    FULL_UPFRONT = "full_upfront"
    DEPOSIT_50 = "deposit_50"
    DEPOSIT_30 = "deposit_30"
    INSTALLMENTS = "installments"
    PAYMENT_ON_DELIVERY = "payment_on_delivery"
    NET_30 = "net_30"
    CUSTOM = "custom"

    CHOICES: ClassVar = [
        (FULL_UPFRONT, "Full Payment Upfront"),
        (DEPOSIT_50, "50% Deposit"),
        (DEPOSIT_30, "30% Deposit"),
        (INSTALLMENTS, "Installments"),
        (PAYMENT_ON_DELIVERY, "Payment on Delivery"),
        (NET_30, "Net 30 Days"),
        (CUSTOM, "Custom Terms"),
    ]


class ValidationLimits:
    """Validation limits for various fields."""

    MIN_BUDGET = 50000
    MAX_BUDGET = 10000000

    MIN_SERVICE_COST = 1000
    MAX_SERVICE_COST = 5000000
    MAX_HOURLY_RATE = 50000

    MIN_ESTIMATED_HOURS = 0.25
    MAX_ESTIMATED_HOURS = 168


class Messages:
    """Standard API response messages."""

    SUCCESS = "Operation completed successfully"
    CREATED = "Resource created successfully"
    UPDATED = "Resource updated successfully"
    DELETED = "Resource deleted successfully"

    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = "Unauthorized access"
    BAD_REQUEST = "Bad request"
    VALIDATION_ERROR = "Validation error"


class WeddingProgressDefaults:
    """Default values for wedding progress stats and calculations."""

    ESSENTIAL_VENDOR_CATEGORIES: ClassVar = [
        VendorCategory.VENUE,
        VendorCategory.CATERING,
        VendorCategory.PHOTOGRAPHY,
        VendorCategory.MUSIC_DJ,
        VendorCategory.DECORATIONS,
    ]

    RECOMMENDED_VENDOR_CATEGORIES: ClassVar = [
        VendorCategory.VENUE,
        VendorCategory.CATERING,
        VendorCategory.PHOTOGRAPHY,
        VendorCategory.MUSIC_DJ,
        VendorCategory.DECORATIONS,
        VendorCategory.ATTIRE,
    ]

    DEFAULT_BUDGET = 500000
    BUDGET_WEDDING_THRESHOLD = 800000
    HIGH_END_WEDDING_THRESHOLD = 1500000

    INVITATION_WEEKS = 12
    VENDOR_BOOKING_WEEKS = 8
    VENUE_WALKTHROUGH_WEEKS = 4
    HEADCOUNT_CONFIRMATION_WEEKS = 2
    FINAL_PREPARATION_WEEKS = 1

    DAYS_THRESHOLD = 7
    WEEKS_THRESHOLD = 14

    EARLY_STAGE_PROGRESS = 0.25
    MID_STAGE_PROGRESS = 0.50
    LATE_STAGE_PROGRESS = 0.75

    EARLY_STAGE_SPENDING = 0.15
    MID_STAGE_SPENDING = 0.35
    LATE_STAGE_SPENDING = 0.60
    FINAL_STAGE_SPENDING = 0.80


class TaskCategory:
    """Task category choices for wedding planning context."""

    VENUE = "venue"
    CATERING = "catering"
    PHOTOGRAPHY = "photography"
    MUSIC = "music"
    FLOWERS = "flowers"
    DECORATIONS = "decorations"
    INVITATIONS = "invitations"
    TRANSPORTATION = "transportation"
    ACCOMMODATIONS = "accommodations"
    ATTIRE = "attire"
    BEAUTY = "beauty"
    DOCUMENTATION = "documentation"
    BUDGET = "budget"
    GENERAL = "general"

    CHOICES = [
        (VENUE, "Venue"),
        (CATERING, "Catering"),
        (PHOTOGRAPHY, "Photography"),
        (MUSIC, "Music"),
        (FLOWERS, "Flowers"),
        (DECORATIONS, "Decorations"),
        (INVITATIONS, "Invitations"),
        (TRANSPORTATION, "Transportation"),
        (ACCOMMODATIONS, "Accommodations"),
        (ATTIRE, "Attire"),
        (BEAUTY, "Beauty"),
        (DOCUMENTATION, "Documentation"),
        (BUDGET, "Budget"),
        (GENERAL, "General"),
    ]

    VALID_CHOICES = [
        VENUE,
        CATERING,
        PHOTOGRAPHY,
        MUSIC,
        FLOWERS,
        DECORATIONS,
        INVITATIONS,
        TRANSPORTATION,
        ACCOMMODATIONS,
        ATTIRE,
        BEAUTY,
        DOCUMENTATION,
        BUDGET,
        GENERAL,
    ]
