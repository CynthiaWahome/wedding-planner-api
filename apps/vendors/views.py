"""Vendor Management views for the Wedding Planning API.

Provides CRUD operations for wedding vendors including creation,
listing, update, and deletion with proper authentication and ownership.
"""

from django.db import models
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.common.responses import APIResponse

from .docs import (
    vendor_create_docs,
    vendor_delete_docs,
    vendor_list_docs,
    vendor_retrieve_docs,
    vendor_update_docs,
)
from .models import Vendor
from .serializers import VendorSerializer


@vendor_create_docs
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_vendor(request):
    """Add a new vendor to the wedding."""
    try:
        wedding_profile = request.user.wedding_profile
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    serializer = VendorSerializer(data=request.data)
    if serializer.is_valid():
        vendor = serializer.save(wedding_profile=wedding_profile)
        return APIResponse.created(
            data=VendorSerializer(vendor).data,
            message="Vendor added successfully",
        )

    return APIResponse.error(
        errors=list(serializer.errors.values()),
        message="Failed to add vendor",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@vendor_list_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_vendors(request):
    """List all vendors for the authenticated user's wedding."""
    try:
        wedding_profile = request.user.wedding_profile
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    vendors = Vendor.objects.filter(wedding_profile=wedding_profile)

    category = request.GET.get("category")
    if category:
        vendors = vendors.filter(category__icontains=category)

    vendors = vendors.order_by("category", "name")

    return APIResponse.success(
        data=VendorSerializer(vendors, many=True).data,
        message="Vendors retrieved successfully",
    )


@vendor_retrieve_docs
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_vendor(request, vendor_id):
    """Get a specific vendor by ID."""
    try:
        wedding_profile = request.user.wedding_profile
        vendor = Vendor.objects.get(id=vendor_id, wedding_profile=wedding_profile)
        return APIResponse.success(
            data=VendorSerializer(vendor).data,
            message="Vendor retrieved successfully",
        )
    except Exception:
        return APIResponse.not_found(message="Vendor not found")


@vendor_update_docs
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_vendor(request, vendor_id):
    """Update a specific vendor's information."""
    try:
        wedding_profile = request.user.wedding_profile
        vendor = Vendor.objects.get(id=vendor_id, wedding_profile=wedding_profile)
    except Exception:
        return APIResponse.not_found(message="Vendor not found")

    partial = request.method == "PATCH"
    serializer = VendorSerializer(vendor, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return APIResponse.success(
            data=serializer.data,
            message="Vendor updated successfully",
        )

    return APIResponse.error(
        errors=list(serializer.errors.values()),
        message="Vendor update failed",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@vendor_delete_docs
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_vendor(request, vendor_id):
    """Remove a vendor from the wedding."""
    try:
        wedding_profile = request.user.wedding_profile
        vendor = Vendor.objects.get(id=vendor_id, wedding_profile=wedding_profile)
        vendor.delete()
        return APIResponse.success(message="Vendor removed successfully")
    except Exception:
        return APIResponse.not_found(message="Vendor not found")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_categories(request):
    """Get list of vendor categories for the wedding."""
    try:
        wedding_profile = request.user.wedding_profile
        vendors = Vendor.objects.filter(wedding_profile=wedding_profile)

        categories = {}
        for vendor in vendors:
            category = vendor.category
            if category not in categories:
                categories[category] = []
            categories[category].append(vendor.name)

        category_data = []
        for category, vendor_names in categories.items():
            category_data.append(
                {
                    "category": category,
                    "count": len(vendor_names),
                    "vendors": sorted(vendor_names),
                }
            )

        category_data.sort(key=lambda x: x["category"])

        return APIResponse.success(
            data={
                "categories": category_data,
                "total_vendors": vendors.count(),
                "total_categories": len(categories),
            },
            message="Vendor categories retrieved successfully",
        )
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_vendors(request):
    """Search vendors by name, category, or contact person."""
    try:
        wedding_profile = request.user.wedding_profile
        vendors = Vendor.objects.filter(wedding_profile=wedding_profile)

        query = request.GET.get("q", "").strip()
        if query:
            vendors = vendors.filter(
                models.Q(name__icontains=query)
                | models.Q(category__icontains=query)
                | models.Q(contact_person__icontains=query)
            )

        vendors = vendors.order_by("name")

        return APIResponse.success(
            data=VendorSerializer(vendors, many=True).data,
            message="Vendor search completed successfully",
        )
    except Exception:
        return APIResponse.error(
            message="Wedding profile not found. Create a profile first.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
