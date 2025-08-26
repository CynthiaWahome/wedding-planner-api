"""Comprehensive tests for Common utilities."""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from rest_framework import status

from .constants import Messages, RSVPStatus, TaskAssignment, TeamRole, VendorCategory
from .responses import APIResponse
from .validators.base import validate_future_date, validate_positive_amount


class TestConstants:
    """Test constants and choices."""

    def test_task_assignment_choices(self):
        """Test task assignment constants."""
        assert TaskAssignment.BRIDE == "bride"
        assert TaskAssignment.GROOM == "groom"
        assert TaskAssignment.COUPLE == "couple"

        choices = TaskAssignment.CHOICES
        assert len(choices) == 3
        assert ("bride", "Bride") in choices
        assert ("groom", "Groom") in choices
        assert ("couple", "Couple") in choices

    def test_rsvp_status_choices(self):
        """Test RSVP status constants."""
        assert RSVPStatus.INVITED == "invited"
        assert RSVPStatus.CONFIRMED == "confirmed"
        assert RSVPStatus.DECLINED == "declined"
        assert RSVPStatus.MAYBE == "maybe"

        choices = RSVPStatus.CHOICES
        assert len(choices) == 4
        assert ("invited", "Invited") in choices
        assert ("confirmed", "Confirmed") in choices
        assert ("declined", "Declined") in choices
        assert ("maybe", "Maybe") in choices

    def test_vendor_category_choices(self):
        """Test vendor category constants."""
        assert VendorCategory.VENUE == "venue"
        assert VendorCategory.CATERING == "catering"
        assert VendorCategory.PHOTOGRAPHY == "photography"
        assert VendorCategory.MUSIC == "music"

        choices = VendorCategory.CHOICES
        assert len(choices) == 7
        assert ("venue", "Venue") in choices
        assert ("catering", "Catering") in choices
        assert ("photography", "Photography") in choices

    def test_team_role_choices(self):
        """Test team role constants."""
        assert TeamRole.BEST_MAN == "best_man"
        assert TeamRole.BEST_LADY == "best_lady"
        assert TeamRole.BRIDESMAID == "bridesmaid"

        choices = TeamRole.CHOICES
        assert len(choices) == 7
        assert ("best_man", "Best Man") in choices
        assert ("best_lady", "Best Lady") in choices

    def test_messages(self):
        """Test API messages."""
        assert Messages.SUCCESS == "Operation completed successfully"
        assert Messages.CREATED == "Resource created successfully"
        assert Messages.NOT_FOUND == "Resource not found"
        assert Messages.UNAUTHORIZED == "Unauthorized access"


class TestValidators:
    """Test custom validators."""

    def test_validate_future_date_valid(self):
        """Test future date validation with valid date."""
        future_date = date.today() + timedelta(days=30)
        # Should not raise any exception
        validate_future_date(future_date)

    def test_validate_future_date_today(self):
        """Test future date validation with today's date."""
        today = date.today()
        with pytest.raises(ValidationError) as excinfo:
            validate_future_date(today)
        assert "must be in the future" in str(excinfo.value)

    def test_validate_future_date_past(self):
        """Test future date validation with past date."""
        past_date = date.today() - timedelta(days=30)
        with pytest.raises(ValidationError) as excinfo:
            validate_future_date(past_date)
        assert "must be in the future" in str(excinfo.value)

    def test_validate_positive_amount_valid_int(self):
        """Test positive amount validation with valid integer."""
        # Should not raise any exception
        validate_positive_amount(100)

    def test_validate_positive_amount_valid_decimal(self):
        """Test positive amount validation with valid decimal."""
        # Should not raise any exception
        validate_positive_amount(Decimal("100.50"))

    def test_validate_positive_amount_zero(self):
        """Test positive amount validation with zero."""
        with pytest.raises(ValidationError) as excinfo:
            validate_positive_amount(0)
        assert "must be greater than zero" in str(excinfo.value)

    def test_validate_positive_amount_negative(self):
        """Test positive amount validation with negative amount."""
        with pytest.raises(ValidationError) as excinfo:
            validate_positive_amount(-50)
        assert "must be greater than zero" in str(excinfo.value)

    def test_validate_positive_amount_negative_decimal(self):
        """Test positive amount validation with negative decimal."""
        with pytest.raises(ValidationError) as excinfo:
            validate_positive_amount(Decimal("-25.75"))
        assert "must be greater than zero" in str(excinfo.value)


class TestAPIResponse:
    """Test API response utility class."""

    def test_success_response(self):
        """Test successful response creation."""
        response = APIResponse.success(data={"test": "data"}, message="Success message")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Success message"
        assert response.data["data"]["test"] == "data"

    def test_success_response_with_meta(self):
        """Test successful response with metadata."""
        response = APIResponse.success(
            data={"test": "data"}, meta={"pagination": {"page": 1}}
        )

        assert response.data["meta"]["pagination"]["page"] == 1

    def test_success_response_defaults(self):
        """Test successful response with default values."""
        response = APIResponse.success()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Operation completed successfully"
        assert response.data["data"] is None

    def test_created_response(self):
        """Test created response."""
        response = APIResponse.created(data={"id": 1}, message="Resource created")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["success"] is True
        assert response.data["message"] == "Resource created"
        assert response.data["data"]["id"] == 1

    def test_error_response(self):
        """Test error response."""
        response = APIResponse.error(
            message="Error occurred",
            errors=["field error"],
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == "Error occurred"
        assert response.data["errors"] == ["field error"]

    def test_error_response_defaults(self):
        """Test error response with defaults."""
        response = APIResponse.error()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["success"] is False
        assert response.data["message"] == "An error occurred"
        assert response.data["data"] is None

    def test_not_found_response(self):
        """Test 404 not found response."""
        response = APIResponse.not_found(
            message="Resource not found", data={"requested_id": 123}
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["success"] is False
        assert response.data["message"] == "Resource not found"
        assert response.data["data"]["requested_id"] == 123

    def test_unauthorized_response(self):
        """Test 401 unauthorized response."""
        response = APIResponse.unauthorized(message="Access denied")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["success"] is False
        assert response.data["message"] == "Access denied"

    def test_forbidden_response(self):
        """Test 403 forbidden response."""
        response = APIResponse.forbidden(message="Permission denied")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["success"] is False
        assert response.data["message"] == "Permission denied"

    def test_validation_error_response(self):
        """Test validation error response."""
        errors = ["Field is required", "Invalid format"]
        response = APIResponse.validation_error(
            errors=errors, message="Validation failed"
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.data["success"] is False
        assert response.data["message"] == "Validation failed"
        assert response.data["errors"] == errors

    def test_paginated_response(self):
        """Test paginated response."""
        data = [{"id": 1}, {"id": 2}, {"id": 3}]
        response = APIResponse.paginated_response(
            data=data, page=1, per_page=10, total=25, message="Data retrieved"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert response.data["message"] == "Data retrieved"
        assert response.data["data"] == data

        meta = response.data["meta"]["pagination"]
        assert meta["current_page"] == 1
        assert meta["per_page"] == 10
        assert meta["total_items"] == 25
        assert meta["total_pages"] == 3
        assert meta["has_next"] is True
        assert meta["has_previous"] is False

    def test_paginated_response_last_page(self):
        """Test paginated response on last page."""
        response = APIResponse.paginated_response(
            data=[{"id": 21}], page=3, per_page=10, total=21
        )

        meta = response.data["meta"]["pagination"]
        assert meta["current_page"] == 3
        assert meta["total_pages"] == 3
        assert meta["has_next"] is False
        assert meta["has_previous"] is True
