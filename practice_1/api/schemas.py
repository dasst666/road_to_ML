from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        from_attributes = True   # в pydantic v2 это замена orm_mode

class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int

class PostRead(BaseModel):
    id: int
    title: str
    body: str
    author_id: int

    class Config:
        from_attributes = True