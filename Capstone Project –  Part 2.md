## **Capstone Project – Part 2** **Backend Structure: Database Schema & API Endpoints** Part 2 of the Capstone Project focuses on defining the backend blueprint for the Wedding Planning Progress Tracker API. It specifies the database schema, entity relationships, and API endpoints, along with key technical decisions on data integrity, authentication, and performance. This structure will guide the implementation phase by ensuring consistency, scalability, and security.

---

## **DATABASE SCHEMA (ERD)**

1. ### **ENTITIES & RELATIONSHIPS**

   ### **1.1 User**

- ### _Primary key:_ `id` (PK)

- ### Stores authentication details (username, email, password hash)

- ### Relationship: One-to-One with `WeddingProfile`

  ### **1.2 WeddingProfile**

- ### _Primary key:_ `id` (PK)

- ### _Foreign key:_ `user_id` → User

- ### Stores couple details: names, date, venue, budget

- ### Relationship:

  - ### One-to-Many with `Task`

  - ### One-to-Many with `Vendor`

  - ### One-to-Many with `Guest`

  ### **1.3 Task**

- ### _Primary key:_ `id` (PK)

- ### _Foreign keys:_

  - ### `wedding_profile_id` → WeddingProfile

  - ### `vendor_id` → Vendor (nullable)

- ### Fields: title, description, assigned_to (bride/groom/couple), status (complete/incomplete), due_date

- ### Relationship: Optional Many-to-One with `Vendor`

  ### **1.4 Vendor**

- ### _Primary key:_ `id` (PK)

- ### _Foreign key:_ `wedding_profile_id` → WeddingProfile

- ### Fields: name, category, contact_info, notes

- ### Relationship: One-to-Many with `Task` (tasks can be linked to a vendor)

  ### **1.5 Guest**

- ### _Primary key:_ `id` (PK)

- ### _Foreign key:_ `wedding_profile_id` → WeddingProfile

- ### Fields: name, contact_info, RSVP_status (invited/confirmed/declined)

2. **DATA TYPES & CONSTRAINTS**

- All tables have **primary keys** (`id`).
- Foreign keys use **ON DELETE CASCADE** to keep data consistent when a wedding profile is removed.
- Indexed fields: `email` in User, `wedding_date` in WeddingProfile.
- Unique constraints: `email` in User, `WeddingProfile` per User.

---

### **2\. API ENDPOINTS**

| Endpoint                    | HTTP Method | Description                            | Auth Required | Request Body / Params                                           | Response                           |
| --------------------------- | :---------: | -------------------------------------- | :-----------: | --------------------------------------------------------------- | ---------------------------------- |
| `/api/auth/register/`       |    POST     | Register a new user account            |      No       | `{ username, email, password }`                                 | User object \+ token               |
| `/api/auth/login/`          |    POST     | Authenticate user and return token     |      No       | `{ email, password }`                                           | Token \+ user info                 |
| `/api/profile/`             |     GET     | Get current user’s wedding profile     |      Yes      | –                                                               | WeddingProfile object              |
| `/api/profile/`             |    POST     | Create wedding profile                 |      Yes      | `{ names, date, venue, budget }`                                | WeddingProfile object              |
| `/api/profile/`             |     PUT     | Update wedding profile                 |      Yes      | `{ names?, date?, venue?, budget? }`                            | Updated WeddingProfile             |
| `/api/profile/progress/`    |     GET     | Get progress stats (tasks completed %) |      Yes      | –                                                               | `{ readiness_percent, days_left }` |
| `/api/tasks/`               |     GET     | List all tasks for profile             |      Yes      | –                                                               | List of Task objects               |
| `/api/tasks/`               |    POST     | Create new task                        |      Yes      | `{ title, description, assigned_to, due_date, vendor_id? }`     | Task object                        |
| `/api/tasks/{id}/`          |     PUT     | Update task                            |      Yes      | `{ title?, description?, assigned_to?, due_date?, vendor_id? }` | Updated Task                       |
| `/api/tasks/{id}/`          |   DELETE    | Delete task                            |      Yes      | –                                                               | `{ success: true }`                |
| `/api/tasks/{id}/complete/` |    PATCH    | Mark task complete/incomplete          |      Yes      | `{ completed: true/false }`                                     | Updated Task                       |
| `/api/vendors/`             |     GET     | List all vendors                       |      Yes      | –                                                               | List of Vendor objects             |
| `/api/vendors/`             |    POST     | Add a vendor                           |      Yes      | `{ name, category, contact, notes }`                            | Vendor object                      |
| `/api/vendors/{id}/`        |     PUT     | Update vendor details                  |      Yes      | `{ name?, category?, contact?, notes? }`                        | Updated Vendor                     |
| `/api/vendors/{id}/`        |   DELETE    | Delete vendor                          |      Yes      | –                                                               | `{ success: true }`                |
| `/api/guests/`              |     GET     | List all guests                        |      Yes      | –                                                               | List of Guest objects              |
| `/api/guests/`              |    POST     | Add a guest                            |      Yes      | `{ name, email, phone, rsvp_status }`                           | Guest object                       |
| `/api/guests/{id}/`         |     PUT     | Update guest info                      |      Yes      | `{ name?, email?, phone?, rsvp_status? }`                       | Updated Guest                      |
| `/api/guests/{id}/`         |   DELETE    | Remove guest                           |      Yes      | –                                                               | `{ success: true }`                |

---

### **3\. ERD SCREENSHOT**

![][image1]

---

## **4\. KEY TECHNICAL DECISIONS**

- **Database Type:** PostgreSQL (chosen for reliability, ACID compliance, and scalability)
- **Data Types:**
  - IDs → Auto-increment integers (PK)
  - Strings → `varchar` with appropriate length
  - Dates → `date` type
  - Status fields → `enum` (or `char` with fixed allowed values)
- **Indexes:**
  - PKs on all tables
  - Index on `wedding_profile_id` for tasks, vendors, and guests for faster lookups
- **Constraints:**
  - Foreign key constraints for data integrity
  - `NOT NULL` where required (e.g., task title)
  - Unique constraint on `user_id` in `WeddingProfile` (one profile per user)

---

### **5\. NOTES ON AUTHENTICATION & AUTHORIZATION**

- All routes except `register` and `login` require **JWT authentication**.
- Users can only access and modify their own WeddingProfile, tasks, vendors, and guests.
- Authorization checks will be enforced in views/serializers.

---

**CONCLUSION**
The backend blueprint in Part 2 sets a clear technical foundation for development. With the schema, endpoints, and security measures defined, the project is ready to move into implementation with a structured plan that supports growth and maintainability.
