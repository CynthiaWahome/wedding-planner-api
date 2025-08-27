"""Task Management views for the Wedding Planning API.

Provides CRUD operations for wedding tasks including creation,
listing, update, and deletion with proper authentication and ownership.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import APIResponse

from .docs import (
    task_create_docs,
    task_delete_docs,
    task_list_docs,
    task_retrieve_docs,
    task_update_docs,
)
from .models import Task
from .serializers import TaskSerializer


@task_create_docs
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):
    """Create a new wedding task."""
    try:
        wedding_profile = request.user.wedding_profile
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save(wedding_profile=wedding_profile)
        return APIResponse.created(
            data=TaskSerializer(task).data,
            message="Task created successfully",
        )

    return APIResponse.error(
        errors=list(serializer.errors.values()),
        message="Task creation failed",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@task_list_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_tasks(request):
    """List all tasks for the authenticated user's wedding.

    **Query Parameters:**
    - `completed`: Filter by completion status (true/false)
    - `assigned_to`: Filter by assignment (bride/groom/couple)
    """
    try:
        wedding_profile = request.user.wedding_profile
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    tasks = Task.objects.filter(wedding_profile=wedding_profile)

    completed = request.GET.get("completed")
    if completed is not None:
        is_completed = completed.lower() == "true"
        tasks = tasks.filter(is_completed=is_completed)

    assigned_to = request.GET.get("assigned_to")
    if assigned_to:
        tasks = tasks.filter(assigned_to=assigned_to)

    tasks = tasks.order_by("-created_at")

    return APIResponse.success(
        data=TaskSerializer(tasks, many=True).data,
        message="Tasks retrieved successfully",
    )


@task_retrieve_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task(request, task_id):
    """Get a specific task by ID."""
    try:
        wedding_profile = request.user.wedding_profile
        task = Task.objects.get(id=task_id, wedding_profile=wedding_profile)
        return APIResponse.success(
            data=TaskSerializer(task).data,
            message="Task retrieved successfully",
        )
    except Exception:
        return APIResponse.not_found(message="Task not found")


@task_update_docs
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    """Update a specific task."""
    try:
        wedding_profile = request.user.wedding_profile
        task = Task.objects.get(id=task_id, wedding_profile=wedding_profile)
    except Exception:
        return APIResponse.not_found(message="Task not found")

    partial = request.method == "PATCH"
    serializer = TaskSerializer(task, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message="Task updated successfully",
        )

    return APIResponse.error(
        errors=list(serializer.errors.values()),
        message="Task update failed",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@task_delete_docs
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    """Delete a specific task."""
    try:
        wedding_profile = request.user.wedding_profile
        task = Task.objects.get(id=task_id, wedding_profile=wedding_profile)
        task.delete()
        return APIResponse.success(message="Task deleted successfully")
    except Exception:
        return APIResponse.not_found(message="Task not found")


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def toggle_task_completion(request, task_id):
    """Toggle the completion status of a task."""
    try:
        wedding_profile = request.user.wedding_profile
        task = Task.objects.get(id=task_id, wedding_profile=wedding_profile)
        task.is_completed = not task.is_completed
        task.save()
        return APIResponse.success(
            data={
                "id": task.id,
                "title": task.title,
                "is_completed": task.is_completed,
                "updated_at": task.updated_at,
            },
            message="Task completion toggled successfully",
        )
    except Exception:
        return APIResponse.not_found(message="Task not found")
