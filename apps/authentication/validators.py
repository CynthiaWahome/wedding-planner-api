"""Authentication validation functions.

Contains validation logic specific to user authentication, registration,
and profile management for the Wedding Planner API.
"""

import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

User = get_user_model()


def validate_password_strength(password):
    """Validate password meets security requirements for wedding data protection."""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must contain at least one special character.")


def validate_unique_username(username):
    """Validate username is unique in the system."""
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists. Please choose a different one.")


def validate_unique_email(email):
    """Validate email is unique and properly formatted."""
    validate_email(email)
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already registered. Please use a different email.")


def validate_username_format(username):
    """Validate username format follows system requirements."""
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        raise ValidationError(
            "Username can only contain letters, numbers, and underscores."
        )

    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long.")

    if len(username) > 30:
        raise ValidationError("Username cannot exceed 30 characters.")


def validate_kenyan_name(name):
    """Validate name format suitable for Kenyan naming conventions."""
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        raise ValidationError(
            "Name can only contain letters, spaces, hyphens, and apostrophes."
        )

    if len(name.strip()) < 2:
        raise ValidationError("Name must be at least 2 characters long.")

    if len(name.strip()) > 50:
        raise ValidationError("Name cannot exceed 50 characters.")

    if name.strip().count(" ") > 3:
        raise ValidationError("Name cannot have more than 3 spaces.")


def validate_password_confirmation(password, password_confirm):
    """Validate password confirmation matches original password."""
    if password != password_confirm:
        raise ValidationError("Password confirmation does not match.")


def validate_active_user_email_update(user, new_email):
    """Validate email update for existing active users."""
    if new_email != user.email:
        if User.objects.filter(email=new_email).exclude(id=user.id).exists():
            raise ValidationError("Email already in use by another account.")
        validate_email(new_email)
