from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WeddingProfile(models.Model):
    """Stores core wedding details for a couple; 1:1 with User."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wedding_profile",
    )
    wedding_date = models.DateField()
    bride_name = models.CharField(max_length=100)
    groom_name = models.CharField(max_length=100)
    venue = models.CharField(max_length=200, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the wedding profile."""
        return f"{self.bride_name} & {self.groom_name} ({self.wedding_date})"
