from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)

class TaskCreate(TaskBase):
    id: int

class TaskUpdate(TaskBase):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=1000)

class TaskToDB(TaskBase):
    id: int

class TaskPublic(TaskBase):
    id: int

class TaskPublicNoID(TaskBase):
    pass