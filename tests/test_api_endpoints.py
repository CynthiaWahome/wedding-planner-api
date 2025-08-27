#!/usr/bin/env python3
"""
Automated API Testing Script for Wedding Planner API
Tests all endpoints to verify they work correctly
"""

from datetime import datetime

import requests

BASE_URL = "http://127.0.0.1:8000"
headers = {"Content-Type": "application/json"}
auth_token = None


def log_test(endpoint: str, method: str, status: str, message: str = ""):
    """Log test results"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {method} {endpoint} - {status} {message}")


def test_user_registration():
    """Test user registration"""
    global headers
    url = f"{BASE_URL}/api/v1/auth/register/"
    data = {
        "username": "aisha_test",
        "email": "aisha.test@gmail.com",
        "password": "TestPassword123",
        "password_confirm": "TestPassword123",
        "first_name": "Aisha",
        "last_name": "Juma",
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code in [201, 400]:
            log_test(
                "/auth/register/", "POST", "✅ PASS", f"Status: {response.status_code}"
            )
            return True
        else:
            log_test(
                "/auth/register/", "POST", "❌ FAIL", f"Status: {response.status_code}"
            )
            return False
    except Exception as e:
        log_test("/auth/register/", "POST", "❌ ERROR", str(e))
        return False


def test_user_login():
    """Test user login and get token"""
    global auth_token, headers
    url = f"{BASE_URL}/api/v1/auth/login/"
    data = {"username": "aisha_test", "password": "TestPassword123"}

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get("success") and "tokens" in result.get("data", {}):
                auth_token = result["data"]["tokens"]["access"]
                headers["Authorization"] = f"Bearer {auth_token}"
                log_test("/auth/login/", "POST", "✅ PASS", "Got access token")
                return True
        log_test("/auth/login/", "POST", "❌ FAIL", f"Status: {response.status_code}")
        return False
    except Exception as e:
        log_test("/auth/login/", "POST", "❌ ERROR", str(e))
        return False


def test_profile_endpoints():
    """Test wedding profile CRUD operations"""
    if not auth_token:
        return False

    url = f"{BASE_URL}/api/v1/profiles/"
    data = {
        "wedding_date": "2026-06-20",
        "bride_name": "Aisha Juma",
        "groom_name": "Vincent Simiyu",
        "venue": "Windsor Golf Hotel & Country Club",
        "budget": 750000.00,
    }

    profile_id = None
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            profile_id = result["data"]["id"]
            log_test("/profiles/", "POST", "✅ PASS", "Profile created")
        else:
            log_test("/profiles/", "POST", "❌ FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        log_test("/profiles/", "POST", "❌ ERROR", str(e))
        return False

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            log_test("/profiles/", "GET", "✅ PASS")
        else:
            log_test("/profiles/", "GET", "❌ FAIL", f"Status: {response.status_code}")
    except Exception as e:
        log_test("/profiles/", "GET", "❌ ERROR", str(e))

    if profile_id:
        try:
            response = requests.get(f"{url}{profile_id}/", headers=headers)
            if response.status_code == 200:
                log_test(f"/profiles/{profile_id}/", "GET", "✅ PASS")
            else:
                log_test(
                    f"/profiles/{profile_id}/",
                    "GET",
                    "❌ FAIL",
                    f"Status: {response.status_code}",
                )
        except Exception as e:
            log_test(f"/profiles/{profile_id}/", "GET", "❌ ERROR", str(e))

    return True


def test_guest_endpoints():
    """Test guest management endpoints"""
    if not auth_token:
        return False

    url = f"{BASE_URL}/api/v1/guests/"
    data = {
        "name": "Lomuria Lokol",
        "email": "lomuria.lokol@gmail.com",
        "rsvp_status": "invited",
        "plus_one": True,
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            log_test("/guests/", "POST", "✅ PASS", "Guest created")
        else:
            log_test("/guests/", "POST", "❌ FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        log_test("/guests/", "POST", "❌ ERROR", str(e))
        return False

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            log_test("/guests/", "GET", "✅ PASS")
        else:
            log_test("/guests/", "GET", "❌ FAIL", f"Status: {response.status_code}")
    except Exception as e:
        log_test("/guests/", "GET", "❌ ERROR", str(e))

    try:
        response = requests.get(f"{url}statistics/", headers=headers)
        if response.status_code == 200:
            log_test("/guests/statistics/", "GET", "✅ PASS")
        else:
            log_test(
                "/guests/statistics/",
                "GET",
                "❌ FAIL",
                f"Status: {response.status_code}",
            )
    except Exception as e:
        log_test("/guests/statistics/", "GET", "❌ ERROR", str(e))

    return True


def test_task_endpoints():
    """Test task management endpoints"""
    if not auth_token:
        return False

    url = f"{BASE_URL}/api/v1/tasks/"
    data = {
        "title": "Book Marula Studios for Photography",
        "description": "Contact Marula Studios for photography services",
        "assigned_to": "couple",
        "vendor": "Marula Studios",
    }

    task_id = None
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            result = response.json()
            task_id = result["data"]["id"]
            log_test("/tasks/", "POST", "✅ PASS", "Task created")
        else:
            log_test("/tasks/", "POST", "❌ FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        log_test("/tasks/", "POST", "❌ ERROR", str(e))
        return False

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            log_test("/tasks/", "GET", "✅ PASS")
        else:
            log_test("/tasks/", "GET", "❌ FAIL", f"Status: {response.status_code}")
    except Exception as e:
        log_test("/tasks/", "GET", "❌ ERROR", str(e))

    if task_id:
        try:
            response = requests.patch(f"{url}{task_id}/toggle/", headers=headers)
            if response.status_code == 200:
                log_test(f"/tasks/{task_id}/toggle/", "PATCH", "✅ PASS")
            else:
                log_test(
                    f"/tasks/{task_id}/toggle/",
                    "PATCH",
                    "❌ FAIL",
                    f"Status: {response.status_code}",
                )
        except Exception as e:
            log_test(f"/tasks/{task_id}/toggle/", "PATCH", "❌ ERROR", str(e))

    return True


def test_vendor_endpoints():
    """Test vendor management endpoints"""
    if not auth_token:
        return False

    url = f"{BASE_URL}/api/v1/vendors/"
    data = {
        "name": "DJ Spinmaster Entertainment",
        "category": "music",
        "contact_person": "Michael Otieno",
        "phone": "+254712987654",
        "email": "dj@spinmaster.co.ke",
        "notes": "Professional DJ with sound system and lighting",
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            log_test("/vendors/", "POST", "✅ PASS", "Vendor created")
        else:
            log_test("/vendors/", "POST", "❌ FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        log_test("/vendors/", "POST", "❌ ERROR", str(e))
        return False

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            log_test("/vendors/", "GET", "✅ PASS")
        else:
            log_test("/vendors/", "GET", "❌ FAIL", f"Status: {response.status_code}")
    except Exception as e:
        log_test("/vendors/", "GET", "❌ ERROR", str(e))

    try:
        response = requests.get(f"{url}search/?q=music", headers=headers)
        if response.status_code == 200:
            log_test("/vendors/search/", "GET", "✅ PASS")
        else:
            log_test(
                "/vendors/search/", "GET", "❌ FAIL", f"Status: {response.status_code}"
            )
    except Exception as e:
        log_test("/vendors/search/", "GET", "❌ ERROR", str(e))

    try:
        response = requests.get(f"{url}categories/", headers=headers)
        if response.status_code == 200:
            log_test("/vendors/categories/", "GET", "✅ PASS")
        else:
            log_test(
                "/vendors/categories/",
                "GET",
                "❌ FAIL",
                f"Status: {response.status_code}",
            )
    except Exception as e:
        log_test("/vendors/categories/", "GET", "❌ ERROR", str(e))

    return True


def main():
    """Run all API tests"""
    print("🚀 Starting Wedding Planner API Tests")
    print("=" * 50)

    print("\n📝 Testing Authentication...")
    test_user_registration()
    if not test_user_login():
        print("❌ Authentication failed. Cannot continue with protected endpoints.")
        return

    print("\n👤 Testing Profile Management...")
    test_profile_endpoints()

    print("\n👥 Testing Guest Management...")
    test_guest_endpoints()

    print("\n📋 Testing Task Management...")
    test_task_endpoints()

    print("\n🏪 Testing Vendor Management...")
    test_vendor_endpoints()

    print("\n" + "=" * 50)
    print("✅ API Testing Complete!")


if __name__ == "__main__":
    main()
