from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal, get_db
from db.models.book import Book
from schemas.task_parse_text import TaskResult
from schemas.book import BookCreate, BookRead, BookUpdate
from workers.tasks import hello, parse_text
from workers.schemas.text import TextIn
from workers.celery_app import celery_app


app = FastAPI()

@app.post("/books/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    # book = Book(title=payload.title, author=payload.author)
    book = Book(**payload.model_dump())
    db.add(book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Такая книга уже существует")
    db.refresh(book)
    return book

@app.patch("/books/{book_id}", response_model=BookRead)
async def update_book(payload: BookUpdate, book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Такой книги не существует")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(book, k, v)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Такая книга уже существует")
    db.refresh(book)
    return book


@app.get("/books/")
def read_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@app.get("/books/{book_id}")
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Такой книги не существует")

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book:
        db.delete(book)
        db.commit()
        return {"success": True}
    else:
        raise HTTPException(status_code=404, detail="Такой книги не существует")

class HelloIn(BaseModel):
    name: str

@app.post("/enqueue")
def enqueue_task(payload: HelloIn):
    task = hello.delay(payload.name)
    return {"task_id": task.id, "state": "queued"}

@app.get("/result/{task_id}")
def get_result(task_id: str):
    res = hello.AsyncResult(task_id)
    if res.state == "PENDING":
        return {"state": res.state}
    if res.state == "FAILURE":
        return {"state": res.state, "error": str(res.info)}
    return {"state": res.state, "result": res.result}


@app.post("/enqueue-text")
def enqueue_parse_task(payload: TextIn, db: Session = Depends(get_db)):
    task = parse_text.delay(payload.text)
    row = TaskResult(
        task_id=task.id,
        status="QUEUED",
        input_text=payload.text,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return {"task_id": task.id, "state": "queued"}

@app.get("/result-text/{task_id}")
def get_parse_result(task_id: str, db: Session = Depends(get_db)):
    res = parse_text.AsyncResult(task_id, app=celery_app)
    row = db.execute(
        select(TaskResult).where(TaskResult.task_id == task_id)
    ).scalar_one_or_none

    body = {"task_id": task_id, "state": res.state}
    if row:
        body.update({
            "db_status": row.status,
            "result": row.result,
            "error": row.error,
            "created_at": row.created_at,
            "finished_at": row.finished_at,
        })
    # if res.state == "PENDING":
    #     return {"state": res.state}
    # if res.state == "FAILURE":
    #     return {"state": res.state, "error": str(res.info)}
    # return {"state": res.state, "result": res.result}
    return body