"""URL configuration for vendors app.

Defines endpoints for vendor management including creation,
listing, update, deletion, and vendor analytics.
"""

from django.urls import path

from . import views

app_name = "vendors"

urlpatterns = [
    path("", views.create_vendor, name="create_vendor"),
    path("list/", views.list_vendors, name="list_vendors"),
    path("<int:vendor_id>/", views.get_vendor, name="get_vendor"),
    path("<int:vendor_id>/update/", views.update_vendor, name="update_vendor"),
    path("<int:vendor_id>/delete/", views.delete_vendor, name="delete_vendor"),
    path("categories/", views.vendor_categories, name="vendor_categories"),
    path("search/", views.search_vendors, name="search_vendors"),
]
