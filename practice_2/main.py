from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.database import SessionLocal, Book
from schemas.book import BookCreate, BookRead, BookUpdate

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

