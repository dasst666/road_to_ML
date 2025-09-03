# app/db/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Sequence, Optional
from practice_1.db.models import User, Post

# USERS
def create_user(db: Session, *, email: str, full_name: str | None = None) -> User:
    obj = User(email=email, full_name=full_name)
    db.add(obj)
    db.flush()           # получим id, но транзакцию не коммитим здесь (делает зависимость)
    db.refresh(obj)
    return obj

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.scalar(stmt)

def list_users(db: Session, limit: int = 50, offset: int = 0) -> Sequence[User]:
    stmt = select(User).limit(limit).offset(offset)
    return db.scalars(stmt).all()

# POSTS
def create_post(db: Session, *, title: str, body: str, author_id: int) -> Post:
    obj = Post(title=title, body=body, author_id=author_id)
    db.add(obj)
    db.flush()
    db.refresh(obj)
    return obj

def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.get(Post, post_id)

def list_posts(db: Session, limit: int = 50, offset: int = 0) -> Sequence[Post]:
    stmt = select(Post).order_by(Post.id.desc()).limit(limit).offset(offset)
    return db.scalars(stmt).all()