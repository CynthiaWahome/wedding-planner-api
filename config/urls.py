"""URL configuration for Wedding Planning API.

Main URL router with API versioning and comprehensive endpoint organization.
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin interface
    path("admin/", admin.site.urls),
    # API Documentation (OpenAPI/Swagger)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # API v1 endpoints
    path("api/v1/auth/", include("apps.authentication.urls")),
    # Health check endpoint
    path("health/", lambda request: __import__("django.http").JsonResponse({"status": "healthy"})),
]
