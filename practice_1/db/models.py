from typing import Annotated, Optional, List
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from practice_1.db.base import Base, intpk, str_255

class User(Base):
    id: Mapped[intpk]
    email: Mapped[str_255] = mapped_column(unique=True, index=True)
    full_name: Mapped[Optional[str]] = mapped_column(default=None)

    # lazy="selectin" — удобный режим для последующего selectinload
    posts: Mapped[List["Post"]] = relationship(back_populates="author", lazy="selectin")


class Post(Base):
    id: Mapped[intpk]
    title: Mapped[str_255]
    body: Mapped[str]  # TEXT автоматически подберётся
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    author: Mapped["User"] = relationship(back_populates="posts", lazy="joined")

    # Пример серверного дефолта/таймстампа
    created_at: Mapped[Optional[str]] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )