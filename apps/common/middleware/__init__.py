"""Common middleware for the Wedding Planner API."""

from .logging import RequestLoggingMiddleware

__all__ = ["RequestLoggingMiddleware"]
