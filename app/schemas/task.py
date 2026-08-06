from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        examples=["eg: Buy Grocery."], 
    )

    description: str | None = Field(
        default=None,
        max_length=600,
    )

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int 
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    description: str | None = Field(
        default=None,
        max_length=600,
    )
    completed: bool | None = None