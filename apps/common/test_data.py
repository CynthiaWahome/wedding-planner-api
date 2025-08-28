"""Test data constants for API documentation examples."""

from typing import ClassVar


class TestUserProfiles:
    """Test user profile data for consistent documentation examples."""

    PRIMARY_USER_EMAIL = "aisha.vincent@gmail.com"
    PRIMARY_BRIDE_NAME = "Aisha Juma"
    PRIMARY_GROOM_NAME = "Vincent Simiyu"
    PRIMARY_VENUE = "Windsor Golf Hotel & Country Club"
    PRIMARY_BUDGET = 750000.00
    PRIMARY_WEDDING_DATE = "2026-06-20"

    SECONDARY_USER_EMAIL = "grace.njeri@outlook.com"
    SECONDARY_BRIDE_NAME = "Grace Njeri"
    SECONDARY_GROOM_NAME = "Peter Kiprotich"
    SECONDARY_VENUE = "Safari Park Hotel, Nairobi"
    SECONDARY_BUDGET = 950000.00
    SECONDARY_WEDDING_DATE = "2025-12-15"


class TestGuestData:
    """Test guest data for documentation examples."""

    GUEST_NAMES: ClassVar = [
        "Khadija Ali",
        "Mary Wanjiku",
        "Catherine Muthoni",
        "Kiprotich Cheruiyot",
        "Lomuria Lokol",
    ]

    GUEST_EMAILS: ClassVar = [
        "khadija.ali@gmail.com",
        "mary.wanjiku@gmail.com",
        "catherine.muthoni@outlook.com",
        "kiprotich.cheruiyot@yahoo.com",
        "lomuria.lokol@gmail.com",
    ]


class TestVendorData:
    """Test vendor data for documentation examples."""

    VENDOR_NAMES: ClassVar = [
        "DJ Spinmaster Entertainment",
        "Marula Studios Photography",
        "Tana River Cultural Group",
        "Safari Park Hotel Catering",
    ]

    VENDOR_CONTACTS: ClassVar = [
        "Michael Otieno",
        "Sarah Kimani",
        "Joseph Mburu",
        "Grace Wanjiku",
    ]


class TestTaskData:
    """Test task data for documentation examples."""

    TASK_TITLES: ClassVar = [
        "Book traditional Pokomo drums",
        "Design Kamba beadwork accessories",
        "Book Safari Park Hotel for Reception",
        "Book Marula Studios for Photography",
    ]

    TASK_DESCRIPTIONS: ClassVar = [
        "Find Pokomo drummers for ceremonies!",
        "Commission custom Kamba beadwork",
        "Book Safari Park Hotel venue",
        "Contact Marula Studios for photography services",
    ]
