from typing import ClassVar

from django.db import models

from apps.profiles.models import WeddingProfile
from apps.vendors.models import Vendor


class Task(models.Model):
    """Task linked to a WeddingProfile; can optionally link to a Vendor."""

    ASSIGNED_CHOICES: ClassVar = [
        ("bride", "Bride"),
        ("groom", "Groom"),
        ("couple", "Couple"),
    ]

    wedding_profile = models.ForeignKey(
        WeddingProfile,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.CharField(max_length=10, choices=ASSIGNED_CHOICES)
    is_completed = models.BooleanField(default=False)
    vendor = models.ForeignKey(
        Vendor,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return a string representation of the task."""
        return self.title
