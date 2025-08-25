# **Capstone Project – Part 1** **The Idea and Planning Phase**

## **Project Idea**

**Wedding Planning Progress Tracker API**

A Django REST API that allows couples to register, create a wedding profile, manage tasks, link tasks to vendors, invite guests, and track overall progress toward their wedding date.

The goal is to provide a simple, personalized tool for couples to stay organized, coordinate vendor activities, and monitor wedding readiness. This MVP is intentionally lightweight but designed as the **foundation** for the larger **Wedding Planning SaaS platform**.

---

## **Main Features**

* **User Authentication**
  * Register/Login (JWT based)
* **Wedding Profile Management**
  * Couple details (names, date, venue, budget)
  * Overall progress tracking
* **Task Management**
  * CRUD for wedding tasks
  * Tasks can be assigned to *bride*, *groom*, or *couple*
  * Mark tasks complete / incomplete
  * Optionally link tasks to a vendor
* **Vendor Management**
  * CRUD for vendors (name, category, contact, notes)
  * Vendors can be linked to tasks (e.g., “Cake tasting → Vendor: XYZ Bakery”)
* **Guest Management**
  * CRUD guest list
  * RSVP status (invited, confirmed, declined)
* **Progress Tracking**
  * Readiness % based on tasks completed vs. total tasks
  * Days left until wedding

---

## **API (Optional)**

No external API required.
All data will be managed in our own Django REST API.

---

## **Project Structure (Django Apps & Endpoints)**

**Apps**

* `authentication` → user login/registration
* `profiles` → wedding profile management & progress calculation
* `tasks` → CRUD for tasks \+ optional vendor link
* `vendors` → CRUD for vendor records
* `guests` → CRUD for guest list

**Core Models**

* **User** (Django default auth user)
* **WeddingProfile** (1:1 with User)
* **Task** (FK → WeddingProfile; optional FK → Vendor)
* **Vendor** (FK → WeddingProfile)
* **Guest** (FK → WeddingProfile)

**Sample Endpoints**

* **Authentication**
  * `POST /api/auth/register/`
  * `POST /api/auth/login/`
* **Wedding Profile**
  * `GET /api/profile/`
  * `POST /api/profile/`
  * `PUT /api/profile/`
  * `GET /api/profile/progress/`
* **Tasks**
  * `GET /api/tasks/`
  * `POST /api/tasks/`
  * `PUT /api/tasks/{id}/`
  * `DELETE /api/tasks/{id}/`
  * `PATCH /api/tasks/{id}/complete/`
* **Vendors**
  * `GET /api/vendors/`
  * `POST /api/vendors/`
  * `PUT /api/vendors/{id}/`
  * `DELETE /api/vendors/{id}/`
* **Guests**
  * `GET /api/guests/`
  * `POST /api/guests/`
  * `PUT /api/guests/{id}/`
  * `DELETE /api/guests/{id}/`

---

## **Database Schema (Simplified ERD for Capstone MVP)**

`![][image1]`

---

## **5‑Week Project Plan**

**Week 1: Foundation & Setup**

* Setup Django project, apps, and database models
* GitHub repo with clean structure

**Week 2: Authentication**

* Implement user registration/login with JWT
* Secure endpoints with auth/permissions

**Week 3: Profiles & Tasks**

* CRUD for wedding profile
* CRUD for tasks (with assigned\_to field \+ vendor link)
* Implement progress calculation logic

**Week 4: Vendors & Guests**

* CRUD for vendors
* CRUD for guest list \+ RSVP
* Validation & error handling
* Unit tests for tasks/vendors/guests

**Week 5: Documentation & Deployment**

* Add Swagger/OpenAPI docs
* Deploy to Heroku with PostgreSQL
* Final testing & demo prep
