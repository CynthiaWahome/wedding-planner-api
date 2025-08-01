# 💍 Wedding Planning API

A Django REST API to help couples **plan, organize, and track their wedding progress**.
This is a **Capstone Project (MVP)** designed as the foundation for a future **Wedding Planning SaaS platform**.

---

## 🚀 Features (MVP Scope)

- **Authentication**: User registration & login with JWT.
- **Wedding Profile**: Store couple details, date, budget, and venue.
- **Task Management**: Create/update/delete tasks, mark complete, and track readiness.
- **Guest Management**: Manage guest list and RSVP status.
- **Vendor Management** (MVP lite): Add basic vendors and link them to tasks.

---

## 🛠️ Tech Stack

- **Backend**: Django + Django REST Framework
- **Auth**: JWT (via `djangorestframework-simplejwt`)
- **Database**: PostgreSQL
- **Docs**: Swagger/OpenAPI (via `drf-spectacular`)

---

## 📂 Project Structure

````plaintext
wedding-planning-api/
│
├── apps/
│   ├── authentication/   # Login/Register
│   ├── profiles/         # Wedding profile + progress
│   ├── tasks/            # Tasks + completion tracking
│   ├── guests/           # Guest list + RSVP
│   └── vendors/          # Basic vendor management
│
├── config/               # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── example.env           # Example environment variables
└── README.md
````

---

## ⚙️ Local Setup

1. **Clone repo & setup environment**

   ```bash
   git clone https://github.com/your-username/wedding-planning-api.git
   cd wedding-planning-api
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # venv\Scripts\activate   # Windows
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Copy the example environment file and update as needed:

   ```bash
   cp example.env .env
   # Then edit .env to set your values
   ```

4. **Run migrations & start server**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. **Swagger API Docs**
   Visit: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)

---

## 📅 Roadmap & Progress

| **Week** | **Deliverables**                                         | **Status**        |
|----------|----------------------------------------------------------|-------------------|
| Week 1   | Project setup, models draft, repo structure              | ⬜ Not started    |
| Week 2   | Authentication (JWT), secure endpoints                   | ⬜ Not started    |
| Week 3   | Wedding profile CRUD, task CRUD, progress %              | ⬜ Not started    |
| Week 4   | Guest CRUD + RSVP, vendor CRUD, core tests               | ⬜ Not started    |
| Week 5   | API docs, deployment, demo                               | ⬜ Not started    |

*Update the table above as you progress!*

---

## 🌱 Future Enhancements

- Advanced vendor management (quotes, contracts)
- Team roles & permissions
- Multi-tenancy, subscriptions, analytics
- Mobile app (React Native), real-time updates

---

## 👩🏽‍💻 Author

**cycy** – Backend Capstone Project

---

## 📝 How to Contribute

1. Fork the repo
2. Create your feature branch:
   `git checkout -b feature/YourFeature`
3. Commit your changes:
   `git commit -m 'Add some feature'`
4. Push to the branch:
   `git push origin feature/YourFeature`
5. Open a Pull Request

---

## 📌 Progress Tracker

- [ ] Step 1: Repo setup
- [ ] Step 2: Authentication endpoints
- [ ] Step 3: Profiles + Tasks
- [ ] Step 4: Guests + Vendors
- [ ] Step 5: Docs + Deploy
````
