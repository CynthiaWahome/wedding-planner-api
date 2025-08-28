"""Wedding Profile views for the Wedding Planning API.

Provides CRUD operations for wedding profiles including creation,
retrieval, update, and deletion with proper authentication.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.common.constants import VendorCategory, WeddingProgressDefaults
from apps.common.responses import APIResponse

from .docs import (
    profile_create_docs,
    profile_delete_docs,
    profile_progress_docs,
    profile_retrieve_docs,
    profile_update_docs,
)
from .models import WeddingProfile
from .serializers import WeddingProfileSerializer

User = get_user_model()


def generate_dynamic_milestones(wedding_profile):
    """Generate dynamic milestones based on actual wedding date."""
    from datetime import date, timedelta

    milestones = []
    wedding_date = wedding_profile.wedding_date
    today = date.today()

    invitation_date = wedding_date - timedelta(
        weeks=WeddingProgressDefaults.INVITATION_WEEKS
    )
    if today <= invitation_date:
        days_until = (invitation_date - today).days
        if days_until <= WeddingProgressDefaults.DAYS_THRESHOLD:
            milestones.append(f"Send invitations (in {days_until} days)")
        elif days_until <= WeddingProgressDefaults.WEEKS_THRESHOLD:
            milestones.append(f"Send invitations (in {days_until // 7} weeks)")
        else:
            milestones.append(f"Send invitations (in {days_until // 30} months)")

    vendor_deadline = wedding_date - timedelta(
        weeks=WeddingProgressDefaults.VENDOR_BOOKING_WEEKS
    )
    if today <= vendor_deadline:
        days_until = (vendor_deadline - today).days
        if days_until <= WeddingProgressDefaults.DAYS_THRESHOLD:
            milestones.append(f"Finalize all vendors (in {days_until} days)")
        elif days_until <= WeddingProgressDefaults.WEEKS_THRESHOLD:
            milestones.append(f"Finalize all vendors (in {days_until // 7} weeks)")
        else:
            milestones.append(f"Finalize all vendors (in {days_until // 30} months)")

    venue_date = wedding_date - timedelta(
        weeks=WeddingProgressDefaults.VENUE_WALKTHROUGH_WEEKS
    )
    if today <= venue_date:
        days_until = (venue_date - today).days
        if days_until <= WeddingProgressDefaults.DAYS_THRESHOLD:
            milestones.append(f"Final venue walkthrough (in {days_until} days)")
        elif days_until <= WeddingProgressDefaults.WEEKS_THRESHOLD:
            milestones.append(f"Final venue walkthrough (in {days_until // 7} weeks)")
        else:
            milestones.append(f"Final venue walkthrough (in {days_until // 30} months)")

    headcount_date = wedding_date - timedelta(
        weeks=WeddingProgressDefaults.HEADCOUNT_CONFIRMATION_WEEKS
    )
    if today <= headcount_date:
        days_until = (headcount_date - today).days
        if days_until <= WeddingProgressDefaults.DAYS_THRESHOLD:
            milestones.append(f"Confirm final headcount (in {days_until} days)")
        else:
            milestones.append(f"Confirm final headcount (in {days_until // 7} weeks)")

    final_prep_date = wedding_date - timedelta(
        weeks=WeddingProgressDefaults.FINAL_PREPARATION_WEEKS
    )
    if today <= final_prep_date:
        days_until = (final_prep_date - today).days
        milestones.append(f"Final preparations week (in {days_until} days)")

    if not milestones:
        if today >= wedding_date:
            days_passed = (today - wedding_date).days
            milestones.append(
                f"Wedding completed {days_passed} days ago - Congratulations!"
            )
        else:
            days_until_wedding = (wedding_date - today).days
            milestones.append(f"Wedding day in {days_until_wedding} days!")

    return milestones[:3]


def calculate_vendors_needed(wedding_profile):
    """Calculate dynamic vendor requirements based on wedding details."""
    budget = float(wedding_profile.budget or WeddingProgressDefaults.DEFAULT_BUDGET)

    if budget >= WeddingProgressDefaults.HIGH_END_WEDDING_THRESHOLD:
        vendor_categories = WeddingProgressDefaults.RECOMMENDED_VENDOR_CATEGORIES + [
            VendorCategory.OTHER
        ]
        return len(vendor_categories)  # 7 vendors
    elif budget >= WeddingProgressDefaults.BUDGET_WEDDING_THRESHOLD:
        # Mid-range wedding
        return len(WeddingProgressDefaults.RECOMMENDED_VENDOR_CATEGORIES)
    else:  # Budget wedding
        return len(WeddingProgressDefaults.ESSENTIAL_VENDOR_CATEGORIES)


def calculate_budget_used(
    wedding_profile, vendors_booked, total_tasks, completed_tasks
):
    """Calculate realistic budget usage based on planning progress."""
    from decimal import Decimal

    total_budget = Decimal(
        str(wedding_profile.budget or WeddingProgressDefaults.DEFAULT_BUDGET)
    )

    task_completion_rate = (completed_tasks / total_tasks) if total_tasks > 0 else 0
    vendor_booking_rate = vendors_booked / calculate_vendors_needed(wedding_profile)

    overall_progress = (task_completion_rate + vendor_booking_rate) / 2

    if overall_progress <= WeddingProgressDefaults.EARLY_STAGE_PROGRESS:
        spending_rate = Decimal(str(WeddingProgressDefaults.EARLY_STAGE_SPENDING))
    elif overall_progress <= WeddingProgressDefaults.MID_STAGE_PROGRESS:
        spending_rate = Decimal(str(WeddingProgressDefaults.MID_STAGE_SPENDING))
    elif overall_progress <= WeddingProgressDefaults.LATE_STAGE_PROGRESS:
        spending_rate = Decimal(str(WeddingProgressDefaults.LATE_STAGE_SPENDING))
    else:
        spending_rate = Decimal(str(WeddingProgressDefaults.FINAL_STAGE_SPENDING))

    return int(total_budget * spending_rate)


@profile_create_docs
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_profile(request):
    """Create a new wedding profile for the authenticated user."""
    if hasattr(request.user, "wedding_profile"):
        return APIResponse.error(
            message="User already has a wedding profile",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    serializer = WeddingProfileSerializer(data=request.data)
    if serializer.is_valid():
        profile = serializer.save(user=request.user)
        return APIResponse.created(
            data=WeddingProfileSerializer(profile).data,
            message="Wedding profile created successfully",
        )

    return APIResponse.error(
        errors=list(serializer.errors.values()),
        message="Profile creation failed",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@profile_retrieve_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Get the authenticated user's wedding profile."""
    try:
        profile = request.user.wedding_profile
        return APIResponse.success(
            data=WeddingProfileSerializer(profile).data,
            message="Wedding profile retrieved successfully",
        )
    except WeddingProfile.DoesNotExist:
        return APIResponse.not_found(message="Wedding profile not found")


@profile_update_docs
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update the authenticated user's wedding profile."""
    try:
        profile = request.user.wedding_profile
    except WeddingProfile.DoesNotExist:
        return APIResponse.not_found(message="Wedding profile not found")

    partial = request.method == "PATCH"
    serializer = WeddingProfileSerializer(profile, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message="Wedding profile updated successfully",
        )

    return APIResponse.error(
        errors=list(serializer.errors.values()),
        message="Profile update failed",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@profile_delete_docs
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_profile(request):
    """Delete the authenticated user's wedding profile."""
    try:
        profile = request.user.wedding_profile
        profile.delete()
        return APIResponse.success(message="Wedding profile deleted successfully")
    except WeddingProfile.DoesNotExist:
        return APIResponse.not_found(message="Wedding profile not found")


@profile_progress_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def wedding_progress(request):
    """Get wedding planning progress statistics."""
    try:
        from datetime import date

        from apps.guests.models import Guest
        from apps.tasks.models import Task
        from apps.vendors.models import Vendor

        wedding_profile = request.user.wedding_profile

        tasks = Task.objects.filter(wedding_profile=wedding_profile)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(is_completed=True).count()

        guests = Guest.objects.filter(wedding_profile=wedding_profile)
        total_guests = guests.count()
        confirmed_guests = guests.filter(rsvp_status="confirmed").count()

        vendors = Vendor.objects.filter(wedding_profile=wedding_profile)
        vendors_booked = vendors.count()
        vendors_needed = calculate_vendors_needed(wedding_profile)

        days_remaining = (wedding_profile.wedding_date - date.today()).days

        task_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        guest_progress = (
            (confirmed_guests / total_guests * 100) if total_guests > 0 else 0
        )
        vendor_progress = vendors_booked / vendors_needed * 100
        overall_progress = round((task_progress + guest_progress + vendor_progress) / 3)

        budget_used = calculate_budget_used(
            wedding_profile, vendors_booked, total_tasks, completed_tasks
        )

        return APIResponse.success(
            data={
                "overall_progress": overall_progress,
                "completed_tasks": completed_tasks,
                "total_tasks": total_tasks,
                "confirmed_guests": confirmed_guests,
                "total_guests": total_guests,
                "vendors_booked": vendors_booked,
                "vendors_needed": vendors_needed,
                "days_remaining": days_remaining,
                "budget_used": budget_used,
                "total_budget": float(wedding_profile.budget),
                "next_milestones": generate_dynamic_milestones(wedding_profile),
            },
            message="Wedding progress retrieved successfully",
        )
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
