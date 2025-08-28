"""Task management validation functions.

Contains validation logic specific to wedding planning tasks, deadlines,
and task management.
"""

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.common.constants import TaskCategory, ValidationLimits
from apps.common.validators.base import validate_future_date


def validate_task_title(title):
    """Validate task title format and content."""
    if not title or not title.strip():
        raise ValidationError("Task title is required.")

    title = title.strip()

    if len(title) < 3:
        raise ValidationError("Task title must be at least 3 characters long.")

    if len(title) > 200:
        raise ValidationError("Task title cannot exceed 200 characters.")

    suspicious_patterns = ["<script", "javascript:", "data:"]
    for pattern in suspicious_patterns:
        if pattern.lower() in title.lower():
            raise ValidationError("Task title contains invalid content.")


def validate_task_description(description):
    """Validate task description content and length."""
    if description is None or description == "":
        return  # Description is optional

    description = description.strip()

    if len(description) < 5:
        raise ValidationError(
            "Task description should be at least 5 characters if provided."
        )

    if len(description) > 2000:
        raise ValidationError("Task description cannot exceed 2000 characters.")

    suspicious_patterns = ["<script", "javascript:", "data:"]
    for pattern in suspicious_patterns:
        if pattern.lower() in description.lower():
            raise ValidationError("Task description contains invalid content.")


def validate_task_due_date(due_date, wedding_date=None):
    """Validate task due date is reasonable for wedding planning."""
    if due_date is None:
        return  # Due date is optional

    validate_future_date(due_date)

    today = timezone.now().date()
    max_future = today + timedelta(days=365 * 6)

    if due_date > max_future:
        raise ValidationError(
            "Task due date cannot be more than 6 years in the future."
        )

    if wedding_date:
        max_post_wedding = wedding_date + timedelta(days=90)
        if due_date > max_post_wedding:
            raise ValidationError(
                "Task due date cannot be more than 3 months after the wedding."
            )

        min_pre_wedding = wedding_date - timedelta(days=365 * 5)
        if due_date < min_pre_wedding:
            raise ValidationError(
                "Task due date cannot be more than 5 years before the wedding."
            )


def validate_task_priority(priority):
    """Validate task priority level."""
    from apps.common.constants import ValidationChoices

    if priority not in ValidationChoices.TASK_PRIORITIES:
        choices_str = ", ".join(ValidationChoices.TASK_PRIORITIES)
        raise ValidationError(f"Task priority must be one of: {choices_str}.")


def validate_task_status(status):
    """Validate task status."""
    from apps.common.constants import ValidationChoices

    if status not in ValidationChoices.TASK_STATUSES:
        raise ValidationError(
            f"Task status must be one of: {', '.join(ValidationChoices.TASK_STATUSES)}."
        )


def validate_task_category(category):
    """Validate task category for wedding planning context."""
    if category not in TaskCategory.VALID_CHOICES:
        raise ValidationError(
            f"Task category must be one of: {', '.join(TaskCategory.VALID_CHOICES)}."
        )


def validate_task_assignment(assigned_to, created_by):
    """Validate task assignment logic."""
    pass


def validate_task_completion_date(completion_date, due_date=None):
    """Validate task completion date."""
    if completion_date is None:
        return

    today = timezone.now().date()

    if completion_date > today:
        raise ValidationError("Task completion date cannot be in the future.")

    if due_date:
        max_overdue = due_date + timedelta(days=365)
        if completion_date > max_overdue:
            raise ValidationError(
                "Task completion date is unreasonably far past due date."
            )


def validate_task_estimated_hours(estimated_hours):
    """Validate estimated hours for task completion."""
    if estimated_hours is None:
        return

    if estimated_hours < ValidationLimits.MIN_ESTIMATED_HOURS:
        raise ValidationError(
            f"Estimated hours cannot be less than "
            f"{ValidationLimits.MIN_ESTIMATED_HOURS} hours (15 minutes)."
        )

    if estimated_hours > ValidationLimits.MAX_ESTIMATED_HOURS:
        raise ValidationError(
            f"Estimated hours cannot exceed "
            f"{ValidationLimits.MAX_ESTIMATED_HOURS} hours per task."
        )
