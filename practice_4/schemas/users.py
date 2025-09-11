from typing import Optional
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    name: str
    age: int
# Но в будущем в базе данных самим нельзя давать айди
class UserCreate(UserBase):
    id: int
    password: str = Field(..., min_length=8)

class UserUpdate(UserBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)

class UserInDB(UserBase):
    id: int
    hashed_password: str

class UserPublic(UserBase):
    id: int