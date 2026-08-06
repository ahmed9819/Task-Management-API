from fastapi import FastAPI
from app.api.routers import tasks

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
)

app.include_router(tasks.router)


