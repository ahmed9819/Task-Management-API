# 🚀 Task Management API

A production-oriented **Task Management REST API** built with **FastAPI**, designed using clean backend architecture principles such as **Layered Architecture**, **Repository Pattern**, **Dependency Injection**, asynchronous database access, and **Alembic database migrations**.

The application is containerized using **Docker** and uses **PostgreSQL** as its persistent database.

This project was developed as part of my **Backend Engineering Internship at FlyRankAI** to strengthen backend engineering fundamentals and gain practical experience building maintainable, scalable, and production-oriented backend systems.

---

## 📌 Features

* ✅ Create, Read, Update, and Delete (CRUD) Tasks
* ✅ Async FastAPI endpoints
* ✅ PostgreSQL database integration
* ✅ SQLAlchemy 2.0 Async ORM
* ✅ Alembic database migrations
* ✅ Dependency Injection
* ✅ Repository Pattern
* ✅ Service Layer for business logic
* ✅ Pydantic request & response validation
* ✅ Environment-based configuration
* ✅ Docker containerization
* ✅ Docker Compose orchestration
* ✅ PostgreSQL health checks
* ✅ Persistent PostgreSQL storage using Docker volumes
* ✅ Automatic API documentation with Swagger UI & ReDoc
* ✅ Layered and maintainable project structure

---

# 🏗️ Architecture

The application follows a layered architecture where each layer has a clearly defined responsibility.

```text
                    Client
                      │
                      ▼
              ┌───────────────┐
              │    Router     │
              │   API Layer   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    Service    │
              │ Business Logic│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  Repository   │
              │ Data Access   │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  PostgreSQL   │
              │   Database    │
              └───────────────┘
```

### Layer Responsibilities

**Router / API Layer**

* Handles HTTP requests and responses.
* Defines API endpoints.
* Performs request/response integration with the service layer.

**Service Layer**

* Contains application and business logic.
* Coordinates operations between routers and repositories.
* Keeps business logic separate from HTTP and database concerns.

**Repository Layer**

* Handles database operations.
* Executes queries through SQLAlchemy.
* Keeps database-access logic isolated from the service layer.

**Database Layer**

* Manages asynchronous SQLAlchemy engine and sessions.
* Provides database sessions through FastAPI dependency injection.

---

# 🐳 Docker Architecture

The application runs as multiple services managed by **Docker Compose**.

```text
                    Host Machine
                         │
                         │
                 Docker Compose
                         │
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
   ┌──────────────┐              ┌──────────────┐
   │   taskapi    │              │    taskdb    │
   │              │              │              │
   │   FastAPI    │─────────────▶│  PostgreSQL  │
   │   + Uvicorn  │   network    │              │
   │   Port 8000  │              │   Port 5432  │
   └──────────────┘              └──────┬───────┘
                                        │
                                        ▼
                               postgres_data volume
```

The FastAPI container communicates with PostgreSQL using the Docker Compose service name:

```text
db
```

Therefore, inside the Docker network, the database connection uses:

```text
postgresql+asyncpg://appuser:password@db:5432/tasksdb
```

`localhost` is **not** used for container-to-container database communication because `localhost` inside the API container refers to the API container itself.

---

# 📂 Project Structure

```text
TaskManagementAPI/
│
├── alembic/
│   ├── versions/
│   │   └── <migration_files>
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
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# ⚙️ Tech Stack

| Technology         | Purpose                            |
| ------------------ | ---------------------------------- |
| **Python 3.11**    | Backend programming language       |
| **FastAPI**        | REST API framework                 |
| **Uvicorn**        | ASGI server                        |
| **SQLAlchemy 2.0** | Async ORM and database access      |
| **PostgreSQL 16**  | Relational database                |
| **asyncpg**        | Asynchronous PostgreSQL driver     |
| **Alembic**        | Database schema migrations         |
| **Pydantic v2**    | Request/response validation        |
| **Docker**         | Application containerization       |
| **Docker Compose** | Multi-container orchestration      |
| **Git & GitHub**   | Version control and source hosting |

---

# 🗄️ Database

The application uses **PostgreSQL 16** for persistent data storage.

The database contains the `tasks` table, which stores task information such as:

* `id`
* `title`
* `description`
* `completed`
* `created_at`
* `updated_at`

Database schema changes are managed through **Alembic migrations** rather than manually modifying the database.

### Database Persistence

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

The PostgreSQL container can be recreated while the database remains persisted in the Docker volume.

---

# 🔐 Environment Variables

Sensitive configuration is not hard-coded into the application.

The project uses environment variables for database configuration.

Example `.env`:

```env
DATABASE_URL=postgresql+asyncpg://appuser:postgres@localhost:5432/tasksdb

POSTGRES_USER=appuser
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tasksdb
```

> **Important:** Do not commit `.env` files containing real credentials to GitHub.

The `.env` file is excluded through `.gitignore`.

### Docker Database URL

Inside Docker, the API uses the PostgreSQL service name `db` instead of `localhost`:

```text
postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
```

This allows Docker's internal network to resolve the PostgreSQL container correctly.

---

# 🐳 Docker Setup

## Prerequisites

Make sure the following are installed:

* Docker Desktop
* Docker Compose

Verify the installation:

```bash
docker --version
```

```bash
docker compose version
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/ahmed9819/TaskManagementAPI.git
```

```bash
cd TaskManagementAPI
```

---

## 2. Configure Environment Variables

Create a `.env` file in the project root.

```env
POSTGRES_USER=appuser
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tasksdb
DATABASE_URL=postgresql+asyncpg://appuser:postgres@localhost:5432/tasksdb
```

For Docker Compose, the API container receives the database URL using the PostgreSQL service name:

```text
postgresql+asyncpg://appuser:postgres@db:5432/tasksdb
```

---

# 🏗️ Build the Docker Image

Build the FastAPI application image:

```bash
docker compose build
```

---

# ▶️ Start the Application

Start both the API and PostgreSQL services:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

You should see:

```text
taskapi
taskdb
```

The API will be available at:

```text
http://localhost:8000
```

---

# ❤️ PostgreSQL Health Check

Docker Compose uses a PostgreSQL health check to ensure the database is ready before starting the API.

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
  interval: 5s
  timeout: 5s
  retries: 5
```

The API depends on the database being healthy:

```yaml
depends_on:
  db:
    condition: service_healthy
```

This prevents the API container from starting before PostgreSQL is ready to accept connections.

---

# 🗃️ Running Alembic Migrations

After starting the containers, run the database migrations.

### Option 1 — Run Alembic inside the API container

```bash
docker compose exec api alembic upgrade head
```

This applies all migrations up to the latest version.

To check the current migration:

```bash
docker compose exec api alembic current
```

To view migration history:

```bash
docker compose exec api alembic history
```

---

# 📖 API Documentation

Once the application is running, FastAPI automatically provides interactive API documentation.

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

---

# 📌 API Endpoints

| Method   | Endpoint      | Description           |
| -------- | ------------- | --------------------- |
| `POST`   | `/tasks`      | Create a new task     |
| `GET`    | `/tasks`      | Retrieve all tasks    |
| `GET`    | `/tasks/{id}` | Retrieve a task by ID |
| `PUT`    | `/tasks/{id}` | Update a task         |
| `DELETE` | `/tasks/{id}` | Delete a task         |

---

# 🐘 Access PostgreSQL

You can access the PostgreSQL database directly from the running container:

```bash
docker exec -it taskdb psql -U appuser -d tasksdb
```

List database tables:

```sql
\dt
```

View tasks:

```sql
SELECT * FROM tasks;
```

Exit PostgreSQL:

```sql
\q
```

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

### Rebuild the application

```bash
docker compose build
```

### Rebuild and restart

```bash
docker compose up -d --build
```

### Check container health

```bash
docker ps
```

### Access PostgreSQL

```bash
docker exec -it taskdb psql -U appuser -d tasksdb
```

---

# 💾 Database Persistence

PostgreSQL uses a Docker named volume:

```text
postgres_data
```

The volume persists database data independently of the PostgreSQL container.

Therefore:

```bash
docker compose down
docker compose up -d
```

does not delete the stored database records.

To intentionally remove the database volume as well:

```bash
docker compose down -v
```

> **Warning:** Removing the volume deletes the PostgreSQL data stored in that volume.

---

# 🧠 Key Backend Concepts Practiced

This project was used to apply several backend engineering concepts in a practical application:

* Layered Architecture
* Separation of Concerns
* Repository Pattern
* Service Layer
* Dependency Injection
* Async Programming
* Async SQLAlchemy Sessions
* REST API Design
* Pydantic Validation
* PostgreSQL
* Database Migrations with Alembic
* Environment-based Configuration
* Docker Containerization
* Docker Compose
* Container Networking
* Database Persistence
* Health Checks
* API Documentation
* Error Handling

---

# 🎯 Learning Outcomes

This project strengthened my understanding of how a backend application evolves from a simple CRUD implementation into a more production-oriented system.

Through this project, I learned how to:

* Design a maintainable layered backend architecture.
* Separate API, business logic, and database responsibilities.
* Implement database access through the Repository Pattern.
* Use asynchronous SQLAlchemy sessions with FastAPI.
* Manage PostgreSQL database schema changes using Alembic.
* Configure applications using environment variables.
* Containerize a FastAPI application using Docker.
* Run FastAPI and PostgreSQL as separate services using Docker Compose.
* Configure communication between containers using Docker's internal network.
* Use health checks to control service startup dependencies.
* Persist PostgreSQL data using Docker volumes.
* Build and run a backend application in an isolated containerized environment.

---

# 🔮 Future Improvements

Potential future improvements include:

* JWT Authentication
* User Registration & Login
* Role-Based Access Control (RBAC)
* Refresh Tokens
* Automated Unit & Integration Testing
* CI/CD Pipeline
* Structured Logging
* API Rate Limiting
* Production configuration management
* PostgreSQL connection pooling optimization
* Deployment to a cloud environment

---

# 👨‍💻 Author

**Muhammad Ahmed Bajwa**

Backend Developer

* LinkedIn: http://www.linkedin.com/in/muhammad-ahmed-bajwa-08a160264
* GitHub: https://github.com/ahmed9819

---

## ⭐ If you found this project useful, consider giving it a star.
