"""Request/Response logging middleware for Wedding Planner API."""

import json
import logging
import time
import uuid
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from apps.common.logging_constants import LoggingConstants, SecurityConstants


class RequestLoggingMiddleware:
    """Simple request/response logging middleware for Django 4.2+."""

    def __init__(self, get_response):
        """Initialize the middleware with response handler."""
        self.get_response = get_response
        self.logger = logging.getLogger("apps.requests")
        self.error_logger = logging.getLogger("apps.errors")
        self.is_production = not settings.DEBUG
        self.log_request_bodies = getattr(
            settings, "LOG_REQUEST_BODIES", settings.DEBUG
        )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process each request/response through the middleware."""
        if self._should_skip_logging(request):
            return self.get_response(request)

        request_id = str(uuid.uuid4())[: LoggingConstants.REQUEST_ID_LENGTH]
        request.request_id = request_id
        start_time = time.time()

        self._log_request(request, request_id)
        response = self.get_response(request)
        duration = round((time.time() - start_time) * 1000, 2)
        self._log_response(request, response, request_id, duration)

        return response

    def _should_skip_logging(self, request: HttpRequest) -> bool:
        """Check if request should be excluded from logging."""
        return any(
            request.path.startswith(path) for path in LoggingConstants.EXCLUDED_PATHS
        )

    def _log_request(self, request: HttpRequest, request_id: str) -> None:
        """Log incoming request with user and client information."""
        user_info = self._get_user_info(request)
        client_ip = self._get_client_ip(request)

        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.path,
            "client_ip": client_ip,
        }

        if user_info:
            log_data.update(user_info)

        if self.is_production:
            if request.method in LoggingConstants.ALWAYS_LOG_METHODS:
                self.logger.info(
                    f"[{request_id}] {request.method} {request.path}", extra=log_data
                )
        else:
            self.logger.info(
                f"[{request_id}] {request.method} {request.path} - Started",
                extra=log_data,
            )

            if request.method in ["POST", "PUT", "PATCH"]:
                self._log_request_body(request, request_id)

    def _log_response(
        self,
        request: HttpRequest,
        response: HttpResponse,
        request_id: str,
        duration: float,
    ) -> None:
        """Log response with status code and duration."""
        status_code = response.status_code
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.path,
            "status_code": status_code,
            "duration_ms": duration,
        }

        message = (
            f"[{request_id}] {request.method} {request.path} - "
            f"{status_code} ({duration}ms)"
        )

        if status_code >= 500:
            self.error_logger.error(message, extra=log_data)
        elif status_code >= 400:
            self.logger.warning(message, extra=log_data)
        elif not self.is_production:
            self.logger.info(message, extra=log_data)

    def _log_request_body(self, request: HttpRequest, request_id: str) -> None:
        """Log filtered request body based on configuration."""
        if not self.log_request_bodies:
            return

        try:
            if hasattr(request, "body") and request.body:
                body = json.loads(request.body.decode("utf-8"))
                filtered_body = self._filter_sensitive_data(body)

                self.logger.debug(
                    f"[{request_id}] Request body: {json.dumps(filtered_body)}",
                    extra={"request_id": request_id},
                )
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.logger.debug(
                f"[{request_id}] Request body: <non-JSON data>",
                extra={"request_id": request_id},
            )

    def _filter_sensitive_data(self, data: Any) -> Any:
        """Remove or redact sensitive fields from data."""
        if not isinstance(data, dict):
            return data

        filtered = {}
        for key, value in data.items():
            if key.lower() in SecurityConstants.SENSITIVE_FIELDS:
                filtered[key] = "[REDACTED]"
            elif key.lower() in SecurityConstants.PARTIALLY_REDACTED_FIELDS:
                filtered[key] = self._partially_redact(str(value))
            elif isinstance(value, dict):
                filtered[key] = self._filter_sensitive_data(value)
            elif isinstance(value, list):
                filtered[key] = [self._filter_sensitive_data(item) for item in value]  # type: ignore[assignment]
            else:
                filtered[key] = value

        return filtered

    def _partially_redact(self, value: str) -> str:
        """Partially hide sensitive values like emails."""
        if "@" in value:
            local, domain = value.split("@", 1)
            return f"{local[:3]}***@{domain}"
        elif len(value) > 6:
            return f"{value[:3]}***{value[-2:]}"
        else:
            return "***"

    def _get_client_ip(self, request: HttpRequest) -> str:
        """Extract client IP address from request headers."""
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR", "unknown")

    def _get_user_info(self, request: HttpRequest) -> dict[str, Any]:
        """Get authenticated user information if available."""
        if hasattr(request, "user") and request.user.is_authenticated:
            return {
                "user_id": request.user.id,
                "username": request.user.username,
            }
        return {}
