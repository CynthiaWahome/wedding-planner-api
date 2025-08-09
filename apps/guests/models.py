from typing import ClassVar

from django.db import models

from apps.profiles.models import WeddingProfile


class Guest(models.Model):
    """Guest linked to a WeddingProfile."""

    RSVP_CHOICES: ClassVar = [
        ("invited", "Invited"),
        ("confirmed", "Confirmed"),
        ("declined", "Declined"),
        ("maybe", "Maybe"),
    ]

    wedding_profile = models.ForeignKey(
        WeddingProfile,
        on_delete=models.CASCADE,
        related_name="guests",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    rsvp_status = models.CharField(max_length=10, choices=RSVP_CHOICES, default="invited")
    plus_one = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a string representation of the guest."""
        return f"{self.name} ({self.rsvp_status})"
