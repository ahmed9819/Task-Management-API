from fastapi import FastAPI
from app.api.routers import tasks
from app.api.routers import auth

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
)

app.include_router(tasks.router)
app.include_router(auth.router)

