"""URL configuration for tasks app.

Defines endpoints for task management including creation,
listing, update, deletion, and completion toggling.
"""

from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.create_task, name="create_task"),
    path("list/", views.list_tasks, name="list_tasks"),
    path("<int:task_id>/", views.get_task, name="get_task"),
    path("<int:task_id>/update/", views.update_task, name="update_task"),
    path("<int:task_id>/delete/", views.delete_task, name="delete_task"),
    path("<int:task_id>/toggle/", views.toggle_task_completion, name="toggle_task"),
]
