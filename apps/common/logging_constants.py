"""Minimal logging constants for Wedding Planner API MVP."""


class SecurityConstants:
    """Security fields that should never be logged in wedding planner API."""

    SENSITIVE_FIELDS: set[str] = {
        "password",
        "password_confirmation",
        "current_password",
        "new_password",
        "access_token",
        "refresh_token",
        "token",
        "authorization",
    }

    PARTIALLY_REDACTED_FIELDS: set[str] = {"email", "phone"}


class LoggingConstants:
    """Simple logging configuration for MVP."""

    REQUEST_ID_LENGTH = 8
    ALWAYS_LOG_METHODS: set[str] = {"POST", "PUT", "PATCH", "DELETE"}
    EXCLUDED_PATHS: set[str] = {"/health/", "/admin/jsi18n/"}
