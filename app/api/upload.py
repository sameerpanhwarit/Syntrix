
from fastapi import APIRouter, UploadFile, File, Depends
import os
import uuid

from sqlalchemy.orm import Session

from app.utils.file_parser import extract_text
from app.utils.chunking import chunk_text
from app.services.embeddings import get_embeddings
from app.services.rag import add_documents

from app.db.database import SessionLocal
from app.models.book import Book
from app.core.deps import get_current_user


router = APIRouter()

UPLOAD_DIR = "data/books"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload-book")
async def upload_book(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    book_id = str(uuid.uuid4())

    file_path = os.path.join(UPLOAD_DIR, f"{book_id}_{file.filename}")

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    text = extract_text(file_path, file.filename)

    chunks = chunk_text(text)

    embeddings = get_embeddings(chunks)

    add_documents(chunks, embeddings, book_id)

    new_book = Book(
        id=book_id,
        user_id=user_id,
        title=file.filename,
        file_path=file_path,
        file_size_kb=os.path.getsize(file_path) // 1024
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {
        "message": "Book uploaded successfully",
        "book_id": book_id,
        "filename": file.filename,
        "chunks_created": len(chunks),
        "user_id": user_id
    }