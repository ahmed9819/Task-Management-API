# 🚀 Task Management API

A production-oriented **Task Management REST API** built with **FastAPI**, designed using clean backend engineering practices such as **Layered Architecture**, **Repository Pattern**, **Dependency Injection**, asynchronous database access, and **database migrations with Alembic**.

The application started as an in-memory CRUD API and was progressively extended to use persistent database storage and containerized infrastructure. The current implementation uses **PostgreSQL**, **SQLAlchemy 2.x**, **Alembic**, and **Docker Compose**.

This project was developed as part of my **Backend Engineering Internship at FlyRankAI** to strengthen practical backend engineering skills and understand how production-oriented backend systems are structured, configured, and deployed.

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
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Service Layer  │
                    │ Business Logic  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │Repository Layer │
                    │ DB Operations   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   SQLAlchemy    │
                    │   Async ORM     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    └─────────────────┘
```

### Layer Responsibilities

**API / Router Layer**

Responsible for:

* Handling HTTP requests
* Receiving request data
* Calling the appropriate service
* Returning HTTP responses

**Service Layer**

Responsible for:

* Business logic
* Application-level rules
* Coordinating repository operations

**Repository Layer**

Responsible for:

* Database queries
* Creating, retrieving, updating, and deleting database records
* Abstracting database operations from the service layer

**Database Layer**

Responsible for:

* Creating asynchronous database connections
* Managing SQLAlchemy sessions
* Providing database sessions through FastAPI dependency injection

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
│   │       └── tasks.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── dependencies/
│   │   └── task.py
│   │
│   ├── models/
│   │   └── task.py
│   │
│   ├── repositories/
│   │   └── task.py
│   │
│   ├── schemas/
│   │   └── task.py
│   │
│   ├── services/
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

DATABASE_URL=postgresql+asyncpg://appuser:your_password@localhost:5432/tasksdb
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
POSTGRES_PASSWORD=your_password
POSTGRES_DB=tasksdb
```

Do **not** commit the real `.env` file to GitHub.

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

## 5. Check running containers

```bash
docker compose ps
```

You should see both services running.

You can also use:

```bash
docker ps
```

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
docker exec -it taskapi alembic upgrade head
```

This applies all migrations up to the latest revision.

To check the current migration:

```bash
docker exec -it taskapi alembic current
```

To view migration history:

```bash
docker exec -it taskapi alembic history
```

---

# 🧪 Verify the Database

You can connect directly to PostgreSQL using `psql`:

```bash
docker exec -it taskdb psql -U appuser -d tasksdb
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
```

### ReDoc

```text
http://localhost:8000/redoc
```

### OpenAPI Schema

```text
http://localhost:8000/openapi.json
```

Swagger UI can be used to interactively test the API endpoints.

---

# 📌 API Endpoints

| Method | Endpoint      | Description           |
| ------ | ------------- | --------------------- |
| POST   | `/tasks`      | Create a new task     |
| GET    | `/tasks`      | Retrieve all tasks    |
| GET    | `/tasks/{id}` | Retrieve a task by ID |
| PUT    | `/tasks/{id}` | Update a task         |
| DELETE | `/tasks/{id}` | Delete a task         |

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
docker logs taskapi
```

or:

```bash
docker compose logs api
```

### View PostgreSQL logs

```bash
docker logs taskdb
```

or:

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
docker exec -it taskapi /bin/bash
```

### Connect to PostgreSQL

```bash
docker exec -it taskdb psql -U appuser -d tasksdb
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

Configure the database URL in `.env`:

```env
DATABASE_URL=postgresql+asyncpg://appuser:your_password@localhost:5432/tasksdb
```

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
* Alembic migrations
* Environment-based configuration
* Docker containerization
* Docker Compose
* Container networking
* Service dependencies
* Health checks
* Persistent Docker volumes
* API documentation with OpenAPI
* Error handling
* Request validation with Pydantic

---

# 📈 Engineering Progression

The project was developed incrementally.

### Stage 1 — CRUD API

The initial implementation stored tasks in memory.

```text
Client → FastAPI → In-Memory Data
```

The limitation was that all data disappeared when the application restarted.

### Stage 2 — Database Persistence

The application was connected to a relational database.

```text
Client → FastAPI → Service → Repository → Database
```

This introduced persistent storage and database migrations.

### Stage 3 — Containerization

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

This made the development environment more reproducible and separated application infrastructure from the host machine.

---

# 🔮 Future Improvements

Potential future enhancements include:

* JWT Authentication
* User registration and login
* Password hashing
* Refresh tokens
* Role-Based Access Control (RBAC)
* Unit and integration testing
* CI/CD pipeline
* Structured logging
* Application monitoring
* Production deployment
* Rate limiting
* API versioning

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
* Structure a backend project for maintainability and future scalability

---

# 👨‍💻 Author

**Muhammad Ahmed Bajwa**

Junior Backend Developer

* LinkedIn: [Muhammad Ahmed Bajwa](https://www.linkedin.com/in/muhammad-ahmed-bajwa-08a160264/)
* GitHub: [ahmed9819](https://github.com/ahmed9819)

---

## ⭐ Support

If you found this project useful or interesting, consider giving the repository a ⭐ on GitHub.
