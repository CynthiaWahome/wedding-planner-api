from django.db import models

from apps.profiles.models import WeddingProfile


class Vendor(models.Model):
    """Vendor linked to a WeddingProfile."""

    wedding_profile = models.ForeignKey(
        WeddingProfile,
        on_delete=models.CASCADE,
        related_name="vendors",
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
