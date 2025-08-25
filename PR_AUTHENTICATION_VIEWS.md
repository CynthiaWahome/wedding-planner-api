# feat: implement JWT authentication views and API routing

## Description

This PR implements comprehensive JWT-based authentication views and API routing for the Wedding Planning API, providing the foundation for user management and secure API access.

**Key Features Added:**

- ✅ User registration with automatic JWT token generation
- ✅ User login with credential validation and token response
- ✅ User logout with refresh token blacklisting
- ✅ User profile management endpoints (get/update)
- ✅ Complete API documentation with OpenAPI/Swagger
- ✅ Versioned API structure with proper URL routing
- ✅ Health check endpoint for monitoring

## Related Issue

Part of Wedding Planning API MVP - Authentication layer implementation for secure user access and presentation demo readiness.

## Motivation and Context

**Why this change is required:**

- Users need to register and login to access wedding planning features
- Secure JWT-based authentication is required for API protection
- API documentation is essential for presentation and future development
- Proper URL routing with versioning supports scalable architecture

**Problem this solves:**

- No user authentication system existed
- No secure access control for API endpoints
- No API documentation for demonstration purposes
- No structured routing for different API versions

## How Has This Been Tested?

**Testing Approach:**
✅ **URL Configuration Testing**

- All authentication endpoints properly routed and accessible
- API versioning working correctly (`/api/v1/auth/`)
- Documentation endpoints functional (`/api/docs/`, `/api/redoc/`)

✅ **Authentication Flow Testing**

- User registration creates users with hashed passwords
- JWT tokens generated successfully on registration/login
- Token validation working for protected endpoints
- Refresh token blacklisting prevents reuse after logout

✅ **Code Quality Testing**

- All ruff linting rules passed
- Pre-commit hooks successful
- Proper docstring formatting and import organization
- Type annotations added where required

**Test Environment:**

- Django 4.2.23 + DRF + PostgreSQL
- Python 3.11 with JWT authentication
- Pre-commit hooks with ruff, black formatting

**Manual Testing Results:**

```bash
# URL routing test passed
python -c "from django.urls import reverse; print(reverse('authentication:register'))"
# Output: /api/v1/auth/register/

# Django system check passed
python manage.py check
# Output: System check identified no issues (0 silenced)
```

## Screenshots (API Documentation)

_API documentation will be available at `/api/docs/` and `/api/redoc/` once deployed_

**Available Endpoints:**

- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User authentication
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/token/refresh/` - JWT token refresh
- `GET /api/v1/auth/profile/` - Get user profile
- `PUT/PATCH /api/v1/auth/profile/update/` - Update profile
- `GET /api/docs/` - Swagger UI documentation
- `GET /api/redoc/` - ReDoc documentation
- `GET /health/` - Health check

## Types of changes

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)

## Technical Implementation Details

### **Authentication Views** (`apps/authentication/views.py`)

#### **1. User Registration**

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # Validates user data, creates user, returns JWT tokens
```

- Password validation with confirmation
- Automatic JWT token generation for immediate login
- Comprehensive error handling with meaningful messages

#### **2. User Authentication**

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Validates credentials, returns user data + JWT tokens
```

- Secure credential validation
- JWT access/refresh token pair generation
- User account status validation

#### **3. Token Management**

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Blacklists refresh token to prevent reuse
```

- Refresh token blacklisting for security
- Graceful error handling for invalid tokens

#### **4. Profile Management**

```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    # Returns current user profile information
```

- JWT-protected endpoint access
- Standardized response format
- Support for profile updates (PUT/PATCH)

## Checklist

- [x] My code follows the code style of this project
- [x] All ruff linting rules passed
- [x] Pre-commit hooks successful
- [x] Comprehensive API documentation added
- [x] JWT authentication properly implemented
- [x] Error handling with meaningful messages
- [x] Input validation using DRF serializers
- [x] Proper permission-based access control
- [x] URL routing with API versioning
- [x] Integration with existing serializers and utilities
- [x] Security best practices followed (password hashing, token blacklisting)
- [x] Consistent API response format maintained
- [x] Health check endpoint added for monitoring
- [x] All new functionality is working and tested
