from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        UniqueConstraint("title", "author", name="uq_book_title_author"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))