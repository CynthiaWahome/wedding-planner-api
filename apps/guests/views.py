"""Guest Management views for the Wedding Planning API.

Provides CRUD operations for wedding guest list including invitation,
RSVP tracking, and guest management with proper authentication and ownership.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import APIResponse

from .docs import (
    guest_create_docs,
    guest_delete_docs,
    guest_list_docs,
    guest_retrieve_docs,
    guest_rsvp_update_docs,
    guest_statistics_docs,
    guest_update_docs,
)
from .models import Guest
from .serializers import GuestSerializer


@guest_create_docs
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_guest(request):
    """Add a new guest to the wedding."""
    try:
        wedding_profile = request.user.wedding_profile
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    serializer = GuestSerializer(data=request.data)
    if serializer.is_valid():
        guest = serializer.save(wedding_profile=wedding_profile)
        return APIResponse.created(
            data=GuestSerializer(guest).data,
            message="Guest added successfully",
        )

    return APIResponse.error(
        errors=list(serializer.errors.values()),
        message="Failed to add guest",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@guest_list_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_guests(request):
    """List all guests for the authenticated user's wedding."""
    try:
        wedding_profile = request.user.wedding_profile
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    guests = Guest.objects.filter(wedding_profile=wedding_profile)

    rsvp_status = request.GET.get("rsvp_status")
    if rsvp_status:
        guests = guests.filter(rsvp_status=rsvp_status)

    plus_one = request.GET.get("plus_one")
    if plus_one is not None:
        has_plus_one = plus_one.lower() == "true"
        guests = guests.filter(plus_one=has_plus_one)

    guests = guests.order_by("name")

    return APIResponse.success(
        data=GuestSerializer(guests, many=True).data,
        message="Guests retrieved successfully",
    )


@guest_retrieve_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_guest(request, guest_id):
    """Get a specific guest by ID."""
    try:
        wedding_profile = request.user.wedding_profile
        guest = Guest.objects.get(id=guest_id, wedding_profile=wedding_profile)
        return APIResponse.success(
            data=GuestSerializer(guest).data,
            message="Guest retrieved successfully",
        )
    except Exception:
        return APIResponse.not_found(message="Guest not found")


@guest_update_docs
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_guest(request, guest_id):
    """Update a specific guest's information."""
    try:
        wedding_profile = request.user.wedding_profile
        guest = Guest.objects.get(id=guest_id, wedding_profile=wedding_profile)
    except Exception:
        return APIResponse.not_found(message="Guest not found")

    partial = request.method == "PATCH"
    serializer = GuestSerializer(guest, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message="Guest updated successfully",
        )

    return APIResponse.error(
        errors=list(serializer.errors.values()),
        message="Guest update failed",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@guest_delete_docs
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_guest(request, guest_id):
    """Remove a guest from the wedding."""
    try:
        wedding_profile = request.user.wedding_profile
        guest = Guest.objects.get(id=guest_id, wedding_profile=wedding_profile)
        guest.delete()
        return APIResponse.success(message="Guest removed successfully")
    except Exception:
        return APIResponse.not_found(message="Guest not found")


@guest_rsvp_update_docs
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_rsvp_status(request, guest_id):
    """Update a guest's RSVP status."""
    try:
        wedding_profile = request.user.wedding_profile
        guest = Guest.objects.get(id=guest_id, wedding_profile=wedding_profile)
    except Exception:
        return APIResponse.not_found(message="Guest not found")

    rsvp_status = request.data.get("rsvp_status")
    if not rsvp_status:
        return APIResponse.error(
            message="RSVP status is required",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    valid_statuses = [choice[0] for choice in Guest.RSVP_CHOICES]
    if rsvp_status not in valid_statuses:
        return APIResponse.error(
            message=f"Invalid RSVP status. Must be one of: {', '.join(valid_statuses)}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    guest.rsvp_status = rsvp_status
    guest.save()

    return APIResponse.success(
        data={
            "id": guest.id,
            "name": guest.name,
            "rsvp_status": guest.rsvp_status,
            "updated_at": guest.updated_at,
        },
        message="RSVP status updated successfully",
    )


@guest_statistics_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def guest_statistics(request):
    """Get guest statistics for the wedding."""
    try:
        wedding_profile = request.user.wedding_profile
        guests = Guest.objects.filter(wedding_profile=wedding_profile)

        total_guests = guests.count()
        confirmed = guests.filter(rsvp_status="confirmed").count()
        declined = guests.filter(rsvp_status="declined").count()
        pending = guests.filter(rsvp_status="invited").count()
        maybe = guests.filter(rsvp_status="maybe").count()
        plus_ones = guests.filter(plus_one=True).count()

        confirmation_rate = (confirmed / total_guests * 100) if total_guests > 0 else 0

        return APIResponse.success(
            data={
                "total_guests": total_guests,
                "confirmed": confirmed,
                "declined": declined,
                "pending": pending,
                "maybe": maybe,
                "plus_ones": plus_ones,
                "confirmation_rate": round(confirmation_rate, 1),
            },
            message="Guest statistics retrieved successfully",
        )
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
