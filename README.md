# Wedding Planning API

![Django](https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white&style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?logo=postgresql&logoColor=white&style=for-the-badge)
![JWT](https://img.shields.io/badge/-JWT-000000?logo=jsonwebtokens&logoColor=white&style=for-the-badge)
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![Ruff](https://img.shields.io/badge/-Ruff-FCC21B?logo=ruff&logoColor=white&style=for-the-badge)
![MyPy](https://img.shields.io/badge/-MyPy-1E293B?logo=python&logoColor=white&style=for-the-badge)
![uv](https://img.shields.io/badge/-uv-DE5FE9?logo=python&logoColor=white&style=for-the-badge)

**Wedding Planning API** is a Django REST API for wedding planning. It helps couples track their progress, manage tasks and guests, organize vendors, and keep track of their budget. The API automatically generates timelines based on the wedding date and suggests vendors based on the budget.

## Table of Contents

- [Key Features](#key-features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configure Environment Variables](#configure-environment-variables)
  - [Run the Application](#run-the-application)
- [API Endpoints](#api-endpoints)
- [Testing & Quality](#testing--quality)
- [Contributing](#contributing)
- [License](#license)

## Key Features

- **JWT Authentication** - Secure user login and registration
- **Progress Tracking** - Track wedding planning progress in real-time
- **Task Management** - Create and manage wedding tasks
- **Guest Management** - Handle RSVPs and guest lists
- **Vendor Management** - Organize and search vendors
- **Budget Tracking** - Monitor wedding expenses
- **Timeline Generation** - Auto-generate planning milestones

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- uv

### Installation

Clone the Repository

```bash
git clone https://github.com/CynthiaWahome/wedding-planning-api.git
cd wedding-planner-api
```

Create virtual environment

```bash
uv venv --python 3.11
source .venv/bin/activate  # Mac/Linux
# .venv\\Scripts\\activate   # Windows
```

Install dependencies

```bash
uv pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp example.env .env
# Edit .env with your database credentials
```

### Run the Application

Set up database

```bash
chmod +x scripts/setup_db.sh
./scripts/setup_db.sh
```

Run migrations and start server

```bash
python manage.py migrate
python manage.py runserver 8000
```

**API Documentation**

- **Swagger Docs**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- **API Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

## API Endpoints

### Authentication

- `POST /api/v1/auth/register/`
- `POST /api/v1/auth/login/`
- `POST /api/v1/auth/logout/`
- `POST /api/v1/auth/token/refresh/`
- `GET /api/v1/auth/profile/`
- `PUT /api/v1/auth/profile/update/`

### Wedding Profile

- `POST /api/v1/profiles/`
- `GET /api/v1/profiles/me/`
- `PUT /api/v1/profiles/me/update/`
- `DELETE /api/v1/profiles/me/delete/`
- `GET /api/v1/profiles/progress/`

### Task Management

- `POST /api/v1/tasks/`
- `GET /api/v1/tasks/list/`
- `GET /api/v1/tasks/{id}/`
- `PUT /api/v1/tasks/{id}/update/`
- `DELETE /api/v1/tasks/{id}/delete/`
- `POST /api/v1/tasks/{id}/toggle/`

### Guest Management

- `POST /api/v1/guests/`
- `GET /api/v1/guests/list/`
- `GET /api/v1/guests/{id}/`
- `PUT /api/v1/guests/{id}/update/`
- `DELETE /api/v1/guests/{id}/delete/`
- `PUT /api/v1/guests/{id}/rsvp/`
- `GET /api/v1/guests/statistics/`

### Vendor Management

- `POST /api/v1/vendors/`
- `GET /api/v1/vendors/list/`
- `GET /api/v1/vendors/{id}/`
- `PUT /api/v1/vendors/{id}/update/`
- `DELETE /api/v1/vendors/{id}/delete/`
- `GET /api/v1/vendors/categories/`
- `GET /api/v1/vendors/search/`

## Testing & Quality

```bash
# Run all quality checks
ruff check .
mypy .
python -m pytest -v
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run quality checks (`ruff check .` and `mypy .`)
5. Run tests (`python -m pytest -v`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

Please make sure all tests pass and code follows our style guidelines before submitting a PR.

## License

This project is licensed under the MIT License.
