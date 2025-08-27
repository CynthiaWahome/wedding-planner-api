# Wedding Planning API

A Django REST API for comprehensive wedding planning with real-time progress tracking, intelligent milestone generation, and dynamic budget calculations.

## Core Features

### Progress Calculation Engine

- Dynamic milestone generation based on actual wedding dates
- Adaptive vendor requirements based on budget complexity (5-7 vendors)
- Real-time budget tracking using precise Decimal calculations
- Progress calculation combining task completion, guest confirmations, and vendor bookings

### Technical Architecture

- **Domain-Driven Design**: Modular app architecture with clear separation of concerns
- **Event-Driven Progress Calculation**: Real-time updates across task/guest/vendor changes
- **Financial Precision**: Decimal-based monetary calculations for accuracy
- **Dynamic Configuration**: Algorithm-based milestone generation vs hardcoded data
- **Security-First**: JWT with refresh tokens, input validation, SQL injection protection
- **Type Safety**: Full MyPy compliance with static type checking
- **Test Pyramid**: Unit tests (75/75) + Integration tests (17/17) + Contract testing
- **API-First Design**: OpenAPI specification drives development

## ⚡ Prerequisites

- **Python 3.11+**
- **PostgreSQL** installed and running (`psql --version`)
- **uv** (Python package manager) - `pip install uv`

---

## API Features

### Core Wedding Planning

- **JWT Authentication** - Secure user registration/login with refresh tokens
- **Wedding Profiles** - Complete couple information with budget tracking
- **Task Management** - Assigned tasks with completion tracking
- **Guest Management** - RSVP status tracking and analytics
- **Vendor Management** - Category-based vendor organization with search

### Automated Features

- **Timeline Generation**: Calculates invitation dates, venue walkthroughs, headcount confirmations based on wedding date
- **Budget Modeling**: Realistic spending patterns (15% → 35% → 60% → 80%) based on planning progress
- **Vendor Optimization**: Suggests 5-7 vendors based on budget complexity
- **Real-time Analytics**: Live progress tracking across tasks, guests, and vendors

---

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Authentication**: JWT with `djangorestframework-simplejwt`
- **Database**: PostgreSQL with optimized queries
- **API Docs**: Swagger/OpenAPI via `drf-spectacular`
- **Code Quality**: Ruff + MyPy + 100% test coverage
- **Money Handling**: Decimal precision for accurate financial calculations

---

## Setup

1. **Clone and setup**

   ```bash
   git clone  https://github.com/CynthiaWahom/wedding-planning-api.git
   cd wedding-planner-api

   # Create virtual environment with uv
   uv venv --python 3.11
   source .venv/bin/activate  # Mac/Linux
   # .venv\\Scripts\\activate   # Windows
   ```

2. **Install dependencies**

   ```bash
   uv pip install -r requirements.txt
   ```

3. **Environment setup**

   ```bash
   cp example.env .env
   # Edit .env with your database credentials
   ```

4. **Database setup (auto-creates database)**

   ```bash
   chmod +x scripts/setup_db.sh
   ./scripts/setup_db.sh
   ```

5. **Run migrations and start**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. **Explore the API**

   - **Swagger Docs**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
   - **API Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

---

## Testing & Quality

```bash
# Run all quality checks
ruff check .                    # Code style
mypy .                         # Type checking
python -m pytest -v           # Unit tests (75/75)
newman run Wedding_Planner_API.postman_collection.json  # API tests (17/17)
```

---


## API Highlights

### Progress Tracking

```bash
GET /api/v1/profiles/progress/
# Returns real-time progress with dynamic milestones like:
# "Send invitations (in 84 days)" - calculated from actual wedding date
# "Budget used: KES 337,500 (45%)" - based on planning progress
```

### Vendor Intelligence

```bash
GET /api/v1/vendors/categories/
# Adapts vendor needs: 5 vendors (budget wedding) to 7 vendors (luxury)
```

### Guest Analytics

```bash
GET /api/v1/guests/statistics/
# Live RSVP tracking affecting overall progress calculation
```

---

## 📂 Project Structure

```
wedding-planner-api/
├── config/              # Django project configuration
│   ├── settings.py      # Environment-specific settings
│   ├── urls.py          # Root URL routing
│   └── wsgi.py/asgi.py  # WSGI/ASGI applications
├── apps/                # Domain-specific applications
│   ├── authentication/ # JWT auth with refresh tokens
│   │   ├── models.py    # User model extensions
│   │   ├── serializers.py # Auth request/response handling
│   │   ├── views.py     # Login/register/refresh endpoints
│   │   └── validators.py # Password/username validation
│   ├── profiles/        # Wedding profile management
│   │   ├── models.py    # WeddingProfile model
│   │   ├── views.py     # Progress calculation engine
│   │   └── validators.py # Date/budget validation
│   ├── tasks/           # Task management system
│   ├── guests/          # Guest & RSVP management
│   ├── vendors/         # Vendor categorization & search
│   └── common/          # Shared utilities
│       ├── constants.py # Business logic constants
│       ├── responses.py # Standardized API responses
│       └── validators/  # Reusable validation logic
├── tests/               # Integration tests
├── scripts/             # Database setup automation
└── logs/                # Application logging
```

## Deployment Architecture

- Environment configurations for development/staging/production
- Database migrations with proper constraints and indexes
- API versioning (`/api/v1/`) for backward compatibility
- Comprehensive logging and error handling
- Security headers and CORS configuration
