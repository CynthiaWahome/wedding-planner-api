"""URL configuration for authentication app.

Defines endpoints for user registration, login, logout and profile management.
All authentication endpoints are JWT-based.
"""

from django.urls import path

from . import views

app_name = "authentication"

urlpatterns = [
    # User Registration & Authentication
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.update_profile, name="update_profile"),
]
