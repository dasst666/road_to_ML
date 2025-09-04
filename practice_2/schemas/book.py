from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)

    @field_validator("title", "author", mode="before")
    @classmethod
    def strip_and_collapse(cls, v: str):
        if not isinstance(v, str):
            raise TypeError("must be a string")
        v = " ".join(v.split())
        return v.strip()

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=100)

    @field_validator("title", "author", mode="before")
    @classmethod
    def strip_and_collapse(cls, v: str):
        if not isinstance(v, str):
            raise TypeError("must be a string")
        v = " ".join(v.split())
        return v.strip()
    
class BookRead(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)