# app/api/routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from practice_1.db.deps import get_db
from practice_1.db import crud
from practice_1.db.models import User, Post
from .routers import UserCreate, UserRead, PostCreate, PostRead  # см. выше где мы их объявили

router = APIRouter(prefix="/api")

@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_ep(payload: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, payload.email):
        raise HTTPException(400, "Email already registered")
    user = crud.create_user(db, email=payload.email, full_name=payload.full_name)
    return user

@router.get("/users", response_model=List[UserRead])
def list_users_ep(db: Session = Depends(get_db)):
    return crud.list_users(db)

@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post_ep(payload: PostCreate, db: Session = Depends(get_db)):
    if not crud.get_user_by_id(db, payload.author_id):
        raise HTTPException(404, "Author not found")
    post = crud.create_post(db, title=payload.title, body=payload.body, author_id=payload.author_id)
    return post

@router.get("/posts", response_model=List[PostRead])
def list_posts_ep(db: Session = Depends(get_db)):
    return crud.list_posts(db)