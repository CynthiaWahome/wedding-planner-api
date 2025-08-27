"""URL configuration for Wedding Planning API.

Main URL router with API versioning and comprehensive endpoint organization.
"""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/v1/auth/", include("apps.authentication.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/v1/tasks/", include("apps.tasks.urls")),
    path("api/v1/guests/", include("apps.guests.urls")),
    path("api/v1/vendors/", include("apps.vendors.urls")),
    path(
        "health/",
        lambda request: HttpResponse(
            '{"status": "healthy"}', content_type="application/json"
        ),
    ),
]
