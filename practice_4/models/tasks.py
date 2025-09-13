from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from database.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), index=True)
    content: Mapped[str] = mapped_column(String(200), index=True)