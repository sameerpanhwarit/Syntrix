from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.book import Book

from app.core.deps import get_current_user

import os


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.delete("/delete-book/{book_id}")
def delete_book(
    book_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(
        Book.id == book_id,
        Book.user_id == user_id
    ).first()

    if not book:
        return {
            "message": "Book not found"
        }

    # delete file
    if os.path.exists(book.file_path):
        os.remove(book.file_path)

    # delete DB row
    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully"
    }