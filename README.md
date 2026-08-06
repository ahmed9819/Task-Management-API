# 🚀 Task Management API

A production-oriented **Task Management REST API** built with **FastAPI**, following clean backend architecture principles such as **Layered Architecture**, **Repository Pattern**, **Dependency Injection**, and **Database Migrations with Alembic**.

This project was developed as part of my **Backend Engineering Internship at FlyRankAI** to strengthen backend engineering fundamentals and learn how production-ready APIs are structured.

---

## 📌 Features

- ✅ Create, Read, Update, and Delete (CRUD) Tasks
- ✅ Async FastAPI Endpoints
- ✅ SQLite Database Integration
- ✅ SQLAlchemy 2.0 Async ORM
- ✅ Alembic Database Migrations
- ✅ Dependency Injection
- ✅ Repository Pattern
- ✅ Service Layer for Business Logic
- ✅ Pydantic Request & Response Validation
- ✅ Automatic API Documentation (Swagger UI & ReDoc)
- ✅ Clean Project Structure
- ✅ Scalable and Maintainable Architecture

---

# 🏗️ Project Architecture

The project follows a layered architecture to keep responsibilities separated and the codebase maintainable.

```
Client
   │
   ▼
Routers (API Layer)
   │
   ▼
Service Layer
(Business Logic)
   │
   ▼
Repository Layer
(Database Operations)
   │
   ▼
SQLite Database
```

Each layer has a single responsibility:

- **Routers** handle HTTP requests and responses.
- **Services** contain business logic.
- **Repositories** communicate with the database.
- **Database** stores application data.

---

# 📂 Project Structure

```
TaskManagementAPI
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── app/
│   ├── api/
│   │   └── routers/
│   │
│   ├── core/
│   │
│   ├── database/
│   │
│   ├── dependencies/
│   │
│   ├── models/
│   │
│   ├── repositories/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   └── main.py
│
├── alembic.ini
├── requirements.txt
└── .gitignore
```

---

# ⚙️ Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API Framework |
| Python | Backend Language |
| SQLAlchemy 2.0 | Async ORM |
| SQLite | Database |
| Alembic | Database Migrations |
| Pydantic | Data Validation |
| Uvicorn | ASGI Server |

---

# 🚀 Getting Started

## Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/TaskManagementAPI.git

cd TaskManagementAPI
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate it

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Alembic Migrations

```bash
alembic upgrade head
```

---

## Run the Server

```bash
uvicorn app.main:app --reload
```

---

# 📖 API Documentation

After starting the server:

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 📌 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

---

# 💡 Key Backend Concepts Practiced

- Clean Architecture Principles
- Layered Architecture
- Repository Pattern
- Dependency Injection
- Async Programming
- SQLAlchemy Async Sessions
- Request Validation
- Response Serialization
- Database Migrations
- REST API Design
- Separation of Concerns
- Error Handling
- API Documentation

---

# 📈 Future Improvements

- JWT Authentication
- User Registration & Login
- Role-Based Authorization (RBAC)
- Refresh Tokens
- Docker Containerization
- PostgreSQL Support
- Unit & Integration Testing
- CI/CD Pipeline
- Logging
- Environment-based Configuration

---

# 🎯 Learning Outcome

This project helped strengthen my understanding of building scalable backend systems by applying software engineering best practices instead of placing all logic inside route handlers.

I learned how to:

- Design maintainable backend architecture
- Separate business logic from database operations
- Manage database schema changes using Alembic
- Build asynchronous APIs with FastAPI
- Structure projects for scalability and long-term maintainability

---

# 👨‍💻 Author

**Muhammad Ahmed Bajwa**

Backend Developer

- LinkedIn: www.linkedin.com/in/muhammad-ahmed-bajwa-08a160264
- GitHub: https://github.com/ahmed9819

---

## ⭐ If you found this project helpful, consider giving it a star.