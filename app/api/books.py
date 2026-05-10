from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.book import Book

from app.core.deps import get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/my-books")
def get_my_books(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    books = db.query(Book).filter(
        Book.user_id == user_id
    ).all()

    result = []

    for book in books:

        result.append({
            "book_id": book.id,
            "title": book.title,
            "file_path": book.file_path,
            "file_size_kb": book.file_size_kb,
            "uploaded_at": book.uploaded_at
        })

    return {
        "total_books": len(result),
        "books": result
    }