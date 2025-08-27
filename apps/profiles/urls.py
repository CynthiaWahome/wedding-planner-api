"""URL configuration for wedding profiles app.

Defines endpoints for wedding profile management including
creation, retrieval, update, and deletion operations.
"""

from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("", views.create_profile, name="create_profile"),
    path("me/", views.get_profile, name="get_profile"),
    path("me/update/", views.update_profile, name="update_profile"),
    path("me/delete/", views.delete_profile, name="delete_profile"),
    path("progress/", views.wedding_progress, name="wedding_progress"),
]
