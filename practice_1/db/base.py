# app/db/base.py
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from sqlalchemy import MetaData, String, Integer

# Необязательно, но полезно: единые соглашения имён для Alembic
metadata_obj = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

class Base(DeclarativeBase):
    metadata = metadata_obj

    # автоматическое имя таблицы: User -> users
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

# Часто используемые типы колонок
intpk = Annotated[int, mapped_column(Integer, primary_key=True, index=True)]
str_255 = Annotated[str, mapped_column(String(255))]