from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

from db.models.book import Book
