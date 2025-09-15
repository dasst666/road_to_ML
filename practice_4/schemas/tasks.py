from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from models.tasks import StatusEnum

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    status: StatusEnum = StatusEnum.todo

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=1000)

class TaskPublic(TaskBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
