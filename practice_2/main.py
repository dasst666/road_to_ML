from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal
from schemas.book import BookCreate, BookRead, BookUpdate
from tasks import hello, parse_text
from db.models.book import Book

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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



class TextIn(BaseModel):
    text: str

@app.post("/enqueue-text")
def enqueue_parse_task(payload: TextIn):
    task = parse_text.delay(payload.text)
    return {"task_id": task.id, "state": "queued"}

@app.get("/result-text/{task_id}")
def get_parse_result(task_id: str):
    res = parse_text.AsyncResult(task_id)
    if res.state == "PENDING":
        return {"state": res.state}
    if res.state == "FAILURE":
        return {"state": res.state, "error": str(res.info)}
    return {"state": res.state, "result": res.result}