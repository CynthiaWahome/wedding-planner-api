"""URL configuration for guests app.

Defines endpoints for guest management including invitation,
RSVP tracking, and guest statistics.
"""

from django.urls import path

from . import views

app_name = "guests"

urlpatterns = [
    path("", views.create_guest, name="create_guest"),
    path("list/", views.list_guests, name="list_guests"),
    path("<int:guest_id>/", views.get_guest, name="get_guest"),
    path("<int:guest_id>/update/", views.update_guest, name="update_guest"),
    path("<int:guest_id>/delete/", views.delete_guest, name="delete_guest"),
    path("<int:guest_id>/rsvp/", views.update_rsvp_status, name="update_rsvp"),
    path("statistics/", views.guest_statistics, name="guest_statistics"),
]
