# 🚀 Task Management API

A production-oriented **Task Management REST API** built with **FastAPI**, designed using clean backend engineering practices such as **Layered Architecture**, **Repository Pattern**, **Dependency Injection**, asynchronous database access, JWT authentication, user-specific data ownership, and database migrations with Alembic.

The application started as an in-memory CRUD API and was progressively extended into a persistent, containerized, and authenticated backend system using **PostgreSQL**, **SQLAlchemy 2.x**, **Alembic**, **Docker Compose**, and **JWT-based authentication**.

This project was developed as part of my **Backend Engineering Internship at FlyRankAI** to strengthen practical backend engineering skills and understand how production-oriented backend systems are structured, secured, configured, and deployed.

---

## 📌 Features

* ✅ Create, Read, Update, and Delete (CRUD) Tasks
* ✅ FastAPI REST API
* ✅ Asynchronous API endpoints
* ✅ PostgreSQL database
* ✅ SQLAlchemy 2.x Async ORM
* ✅ Alembic database migrations
* ✅ Repository Pattern
* ✅ Service Layer for business logic
* ✅ Dependency Injection
* ✅ Pydantic v2 request/response validation
* ✅ Async database sessions with `asyncpg`
* ✅ JWT-based authentication
* ✅ Protected API routes
* ✅ JWT token verification
* ✅ User identification through JWT `sub` claim
* ✅ User-specific task ownership
* ✅ Users can only access their own tasks
* ✅ Protected task CRUD operations
* ✅ Authentication logout route
* ✅ Protected authentication test route
* ✅ Docker containerization
* ✅ Docker Compose orchestration
* ✅ PostgreSQL data persistence using Docker volumes
* ✅ PostgreSQL health checks
* ✅ API container waits for a healthy database
* ✅ Environment-based configuration
* ✅ Automatic API documentation with Swagger UI and ReDoc
* ✅ Clean and maintainable project structure

---

# 🏗️ Architecture

The application follows a layered architecture to separate responsibilities and make the codebase easier to maintain and extend.

```text
                         ┌─────────────────┐
                         │     Client      │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  API / Routers  │
                         │   HTTP Layer    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Service Layer  │
                         │  Business Logic │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │Repository Layer │
                         │  DB Operations  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   SQLAlchemy    │
                         │    Async ORM    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         └─────────────────┘
```

### Authentication Flow

JWT authentication is applied before accessing protected endpoints.

```text
                    ┌─────────────────┐
                    │      Client     │
                    └────────┬────────┘
                             │
                             │ Bearer JWT
                             ▼
                    ┌─────────────────┐
                    │ Authentication  │
                    │   Dependency    │
                    └────────┬────────┘
                             │
                             │ Verify JWT
                             ▼
                    ┌─────────────────┐
                    │   JWT Payload   │
                    │      `sub`      │
                    └────────┬────────┘
                             │
                             │ User ID
                             ▼
                    ┌─────────────────┐
                    │ Protected Task  │
                    │     Route       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Service/Repo    │
                    │ Filter by user  │
                    └─────────────────┘
```

The JWT `sub` claim identifies the authenticated user. The task endpoints use this user ID to ensure that users can only access tasks belonging to them.

---

## Layer Responsibilities

### API / Router Layer

Responsible for:

* Handling HTTP requests
* Receiving request data
* Extracting the authenticated user's identity
* Calling the appropriate service
* Returning HTTP responses

### Authentication Dependency

Responsible for:

* Extracting the Bearer token from the request
* Verifying the JWT
* Rejecting invalid or expired tokens
* Providing the decoded JWT payload to protected routes

### Service Layer

Responsible for:

* Business logic
* Application-level rules
* Checking task ownership through repository queries
* Coordinating repository operations

### Repository Layer

Responsible for:

* Database queries
* Creating, retrieving, updating, and deleting database records
* Filtering tasks by `user_id`
* Abstracting database operations from the service layer

### Database Layer

Responsible for:

* Creating asynchronous database connections
* Managing SQLAlchemy sessions
* Providing database sessions through FastAPI dependency injection

---

# 🔐 Authentication & Authorization

The API uses **JWT (JSON Web Token)** authentication.

A client must provide a valid JWT as a Bearer token when accessing protected endpoints.

Example:

```http
Authorization: Bearer <access_token>
```

The authentication dependency:

```python
get_current_user()
```

extracts and verifies the token.

The authenticated user's ID is obtained from the JWT's:

```text
sub
```

claim.

For example:

```json
{
  "sub": "4ab4bedf-cee9-4181-a854-8d7de7551879",
  "role": "authenticated"
}
```

The `sub` value is converted into a UUID and passed through the task service and repository layers.

### User Ownership

Each task contains a:

```text
user_id
```

column.

This establishes ownership between a task and the authenticated user.

For example:

```text
User A
 ├── Task 1
 ├── Task 2
 └── Task 3

User B
 ├── Task 4
 └── Task 5
```

When User A requests their tasks, the repository only retrieves tasks belonging to User A.

This prevents one authenticated user from accessing another user's tasks.

---

# 🚪 Logout

The API provides:

```http
POST /auth/logout
```

The logout route is responsible for the application's logout operation.

Because JWT access tokens are stateless, logging out does not require deleting a server-side session in the same way a traditional session-based authentication system would.

The client should discard its stored authentication token after logout.

---

# 🐳 Docker Architecture

The application runs as multiple services using Docker Compose.

```text
                   Docker Compose
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
      ┌─────────────┐       ┌─────────────┐
      │   FastAPI   │       │ PostgreSQL  │
      │   taskapi   │──────▶│   taskdb    │
      │   :8000     │       │    :5432    │
      └─────────────┘       └──────┬──────┘
                                   │
                                   ▼
                            Docker Volume
                           postgres_data
```

The FastAPI container communicates with PostgreSQL using the Docker Compose service name:

```text
db
```

Therefore, inside the Docker network the database URL uses:

```text
postgresql+asyncpg://<user>:<password>@db:5432/<database>
```

The browser, however, accesses the FastAPI application through the host machine:

```text
http://localhost:8000
```

---

# 🛠️ Tech Stack

| Technology     | Purpose                               |
| -------------- | ------------------------------------- |
| Python 3.11    | Backend programming language          |
| FastAPI        | REST API framework                    |
| SQLAlchemy 2.x | Async ORM                             |
| PostgreSQL 16  | Relational database                   |
| asyncpg        | PostgreSQL asynchronous driver        |
| Alembic        | Database schema migrations            |
| Pydantic v2    | Data validation and serialization     |
| Uvicorn        | ASGI application server               |
| JWT            | Authentication                        |
| Docker         | Application containerization          |
| Docker Compose | Multi-container orchestration         |
| Git / GitHub   | Version control and source management |

---

# 📂 Project Structure

```text
TaskManagementAPI/
│
├── alembic/
│   ├── versions/
│   │   └── <migration-files>
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   └── routers/
│   │       ├── auth.py
│   │       └── tasks.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── task.py
│   │
│   ├── models/
│   │   ├── task.py
│   │   └── ...
│   │
│   ├── repositories/
│   │   └── task.py
│   │
│   ├── schemas/
│   │   ├── task.py
│   │   └── ...
│   │
│   ├── security/
│   │   └── jwt.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── task_service.py
│   │
│   └── main.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

> The exact project structure may vary slightly depending on the current implementation.

---

# 🗄️ Database

The application currently uses **PostgreSQL 16**.

PostgreSQL runs inside its own Docker container:

```text
Container: taskdb
Port: 5432
Database: tasksdb
```

The application communicates with PostgreSQL through SQLAlchemy's asynchronous engine using `asyncpg`.

### Database Connection

Inside Docker Compose, the application uses:

```text
postgresql+asyncpg://<POSTGRES_USER>:<POSTGRES_PASSWORD>@db:5432/<POSTGRES_DB>
```

The important part is:

```text
@db
```

`db` is the Docker Compose service name and acts as the hostname between the containers.

---

# 💾 Database Persistence

PostgreSQL data is stored using a Docker named volume:

```yaml
volumes:
  postgres_data:
```

The volume is mounted inside the PostgreSQL container at:

```text
/var/lib/postgresql/data
```

This means removing and recreating the PostgreSQL container does **not** remove the database data.

For example:

```bash
docker compose down
docker compose up -d
```

will recreate the containers while keeping the PostgreSQL data stored in the Docker volume.

> **Note:** `docker compose down -v` removes the named volumes and therefore deletes the persisted PostgreSQL data.

---

# 🔐 Environment Variables

Database credentials and configuration are supplied through environment variables rather than hard-coded directly into the application.

Example environment variables:

```env
POSTGRES_USER=appuser
POSTGRES_PASSWORD=your_password
POSTGRES_DB=tasksdb
```

The actual `.env` file is intentionally excluded from Git using `.gitignore`.

A `.env.example` file is provided as a template for developers setting up the project locally.

### Docker Database URL

When the FastAPI application runs inside Docker, it must use the PostgreSQL service name instead of `localhost`:

```text
postgresql+asyncpg://appuser:your_password@db:5432/tasksdb
```

This is because `localhost` inside the API container refers to the API container itself, not the PostgreSQL container.

---

# 🐳 Docker Setup

## Prerequisites

Make sure the following are installed:

* Docker Desktop
* Git

Verify Docker:

```bash
docker --version
```

Verify Docker Compose:

```bash
docker compose version
```

---

# 🚀 Running the Application with Docker

## 1. Clone the repository

```bash
git clone https://github.com/ahmed9819/TaskManagementAPI.git
```

Navigate into the project:

```bash
cd TaskManagementAPI
```

---

## 2. Create the environment file

Create a `.env` file in the project root.

Example:

```env
POSTGRES_USER=appuser
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=tasksdb
DATABASE_URL=postgresql+asyncpg://appuser:your_secure_password@localhost:5432/tasksdb
SUPABASE_URL=your_supabase_url
SUPABASE_PUBLISHABLE_KEY=your_supabase_publishable_key
SUPABASE_JWKS_URL=your_supabase_jwks_url
```

---

## 3. Build the application image

```bash
docker compose build
```

---

## 4. Start the services

```bash
docker compose up -d
```

Docker Compose starts:

```text
taskapi
taskdb
```

The API depends on PostgreSQL becoming healthy before the API container starts.

---

## 5. Run database migrations

```bash
docker compose exec api alembic upgrade head
```

---

## 6. Check running containers

```bash
docker compose ps
```

You should see both services running and PostgreSQL reported as healthy.

---

# ❤️ PostgreSQL Health Check

The PostgreSQL service includes a Docker health check using `pg_isready`.

Example:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
  interval: 5s
  timeout: 5s
  retries: 5
```

The API uses:

```yaml
depends_on:
  db:
    condition: service_healthy
```

This ensures Docker waits for PostgreSQL to report a healthy status before starting the API service.

This is more reliable than simply checking whether the PostgreSQL container has started.

---

# 🔄 Running Alembic Migrations

Alembic is used to manage database schema changes.

When the application is running through Docker, run migrations inside the API container:

```bash
docker compose exec api alembic upgrade head
```

Check the current migration:

```bash
docker compose exec api alembic current
```

View migration history:

```bash
docker compose exec api alembic history
```

---

# 🧪 Verify the Database

You can connect directly to PostgreSQL using `psql`:

```bash
docker compose exec db psql -U appuser -d tasksdb
```

Inside PostgreSQL, list tables:

```sql
\dt
```

View tasks:

```sql
SELECT * FROM tasks;
```

Exit:

```sql
\q
```

---

# 🌐 API Documentation

Once the application is running, open:

### Swagger UI

```text
http://localhost:8000/docs

Screenshots:
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)

```

### ReDoc

```text
http://localhost:8000/redoc
```

### OpenAPI Schema

```text
http://localhost:8000/openapi.json
```

Swagger UI can be used to interactively test the API.

For protected endpoints:

1. Obtain a valid JWT.
2. Click **Authorize** in Swagger UI.
3. Enter the Bearer token.
4. Execute the protected endpoints.

Example:

```text
Bearer <your_access_token>
```

---

# 📌 API Endpoints

## Authentication

| Method | Endpoint               | Description                         |
| ------ | ---------------------- | ----------------------------------- |
| POST   | `/auth/login`          | Authenticate/login                  |
| POST   | `/auth/logout`         | Logout                              |
| GET    | `/auth/test-protected` | Test protected-route authentication |

## Tasks

| Method | Endpoint           | Authentication | Description                         |
| ------ | ------------------ | -------------- | ----------------------------------- |
| POST   | `/tasks`           | 🔐 Required    | Create a task                       |
| GET    | `/tasks`           | 🔐 Required    | Retrieve authenticated user's tasks |
| GET    | `/tasks/{task_id}` | 🔐 Required    | Retrieve user's task by ID          |
| PATCH  | `/tasks/{task_id}` | 🔐 Required    | Update user's task                  |
| DELETE | `/tasks/{task_id}` | 🔐 Required    | Delete user's task                  |

All task endpoints require a valid JWT.

Task queries are scoped to the authenticated user's `user_id`, preventing users from accessing tasks owned by other users.

---

# 🔒 Protected Route Behavior

Without a valid JWT:

```text
GET /tasks
        │
        ▼
401 Unauthorized
```

With a valid JWT:

```text
GET /tasks
Authorization: Bearer <JWT>
        │
        ▼
JWT Verification
        │
        ▼
Extract `sub`
        │
        ▼
Filter tasks by user_id
        │
        ▼
Return user's tasks
```

If a task belongs to another user, it is treated as unavailable to the authenticated user rather than exposing another user's data.

---

# 🐳 Useful Docker Commands

### Start services

```bash
docker compose up -d
```

### Stop services

```bash
docker compose down
```

### Rebuild the application

```bash
docker compose build
```

### Rebuild and start

```bash
docker compose up -d --build
```

### View running containers

```bash
docker compose ps
```

### View API logs

```bash
docker compose logs api
```

### View PostgreSQL logs

```bash
docker compose logs db
```

### Follow API logs

```bash
docker compose logs -f api
```

### Follow PostgreSQL logs

```bash
docker compose logs -f db
```

### Open a shell inside the API container

```bash
docker compose exec api /bin/bash
```

### Connect to PostgreSQL

```bash
docker compose exec db psql -U appuser -d tasksdb
```

---

# 🔌 Local Development Without Docker

Docker is the recommended way to run the complete application, but the API can also be run directly from a Python virtual environment if PostgreSQL is available locally.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the database connection in `.env`.

Run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --reload
```

The API will then be available at:

```text
http://localhost:8000
```

---

# 🧠 Key Backend Concepts Practiced

This project provided practical experience with:

* REST API design
* CRUD operations
* Layered Architecture
* Separation of Concerns
* Repository Pattern
* Service Layer
* Dependency Injection
* Async/Await
* Async SQLAlchemy sessions
* PostgreSQL
* SQL queries
* Database schema design
* User ownership and data isolation
* JWT authentication
* Bearer token authentication
* JWT payload verification
* Protected routes
* Alembic migrations
* Environment-based configuration
* Docker containerization
* Docker Compose
* Container networking
* Health checks
* Persistent Docker volumes
* API documentation with OpenAPI
* Error handling
* Request validation with Pydantic

---

# 📈 Engineering Progression

The project was developed incrementally, evolving from a simple CRUD API into an authenticated backend application.

### Stage 1 — CRUD API

The initial implementation stored tasks in memory.

```text
Client → FastAPI → In-Memory Data
```

The limitation was that all data disappeared when the application restarted.

### Stage 2 — Database Persistence

The application was connected to PostgreSQL.

```text
Client → FastAPI → Service → Repository → PostgreSQL
```

This introduced persistent storage and database migrations.

### Stage 3 — Layered Architecture

The application was separated into different layers:

```text
API
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
Database
```

This improved separation of concerns and made the application easier to maintain.

### Stage 4 — Containerization

The application and database were containerized.

```text
Client
   │
   ▼
FastAPI Container
   │
   ▼
PostgreSQL Container
   │
   ▼
Persistent Docker Volume
```

### Stage 5 — JWT Authentication

Authentication was introduced using JWTs.

```text
Client
   │
   │ Bearer Token
   ▼
JWT Verification
   │
   ▼
Authenticated User
   │
   ▼
Protected API
```

### Stage 6 — User-Specific Task Ownership

Tasks were associated with authenticated users through `user_id`.

```text
Authenticated User
        │
        ▼
     user_id
        │
        ▼
     Task Query
        │
        ▼
Only tasks owned by that user
```

This prevents users from accessing other users' tasks.

---

# 🧪 API Testing

The API was tested using **Swagger UI**.

The following functionality was verified:

* ✅ Authentication/login
* ✅ JWT-protected route
* ✅ Second protected route
* ✅ Create task
* ✅ Retrieve authenticated user's tasks
* ✅ Retrieve task by ID
* ✅ Update task
* ✅ Delete task
* ✅ User-specific task ownership
* ✅ Logout route
* ✅ Unauthorized access handling
* ✅ Dockerized API operation
* ✅ PostgreSQL database operations
* ✅ Alembic migrations

---

# 🎯 Learning Outcomes

This project strengthened my understanding of how backend systems evolve from a simple CRUD application into a more production-oriented architecture.

Through this project, I learned how to:

* Design APIs independently from their storage implementation
* Separate HTTP, business logic, and database responsibilities
* Use the Repository Pattern to abstract database operations
* Build asynchronous APIs and database interactions
* Manage relational database schemas using Alembic
* Containerize applications using Docker
* Orchestrate multiple services using Docker Compose
* Connect containers through Docker's internal networking
* Use health checks to coordinate service startup
* Persist database data using Docker volumes
* Keep sensitive configuration outside the source code
* Implement JWT-based authentication
* Protect API routes using FastAPI dependencies
* Extract authenticated user identity from JWT claims
* Associate database records with authenticated users
* Enforce user-specific data access at the repository layer
* Test protected APIs using Swagger UI

---

# 🔮 Future Improvements

Potential future enhancements include:

* Refresh token rotation
* More comprehensive unit and integration testing
* Automated CI/CD pipeline
* Structured logging
* Application monitoring
* Production deployment
* Rate limiting
* API versioning
* More advanced authorization and RBAC
* Automated test coverage reporting

---

# 👨‍💻 Author

**Muhammad Ahmed Bajwa**

Junior Backend Developer

* LinkedIn: [Muhammad Ahmed Bajwa](https://www.linkedin.com/in/muhammad-ahmed-bajwa-08a160264/)
* GitHub: [ahmed9819](https://github.com/ahmed9819)

---

## ⭐ Support

If you found this project useful or interesting, consider giving the repository a ⭐ on GitHub.
