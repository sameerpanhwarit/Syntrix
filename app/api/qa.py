
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
import uuid

from app.utils.validation import verify_answer
from app.services.embeddings import get_embeddings
from app.services.rag import search
from app.core.llm import call_llm

from app.db.database import SessionLocal
from app.models.book import Book
from app.models.ask_ai import AskAI
from app.core.deps import get_current_user


router = APIRouter()


# =========================
# REQUEST MODEL
# =========================
class QuestionRequest(BaseModel):
    question: str
    book_id: str


# =========================
# DATABASE DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# ASK AI API
# =========================
@router.post("/ask")
def ask_question(
    data: QuestionRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    question = data.question
    book_id = data.book_id

    # =========================
    # VERIFY BOOK OWNERSHIP
    # =========================
    book = db.query(Book).filter(
        Book.id == book_id,
        Book.user_id == user_id
    ).first()

    if not book:
        return {
            "answer": "Unauthorized or book not found"
        }

    # =========================
    # EMBED QUESTION
    # =========================
    query_embedding = get_embeddings([question])[0]

    # =========================
    # SEARCH RELEVANT CHUNKS
    # =========================
    results = search(
        query_embedding,
        book_id=book_id,
        k=5
    )

    if not results:
        return {
            "answer": "No relevant content found in this book."
        }

    # =========================
    # BUILD CONTEXT
    # =========================
    chunks = [r["text"] for r in results[:3]]

    context = "\n\n".join(chunks)

    # =========================
    # STRICT PROMPT
    # =========================
    prompt = f"""
You are a strict AI assistant.

You MUST return ONLY valid JSON.

Format:

{{
  "answer": "final answer from book",
  "evidence": "exact sentence from context"
}}

RULES:
- Use ONLY the provided context
- Do NOT use external knowledge
- Do NOT explain outside context
- If answer not found, return:

{{
  "answer": "NOT IN BOOK",
  "evidence": ""
}}

Context:
{context}

Question:
{question}
"""

    # =========================
    # CALL LLM
    # =========================
    answer_raw = call_llm(prompt)

    # =========================
    # SAFE JSON PARSING
    # =========================
    try:
        answer_json = json.loads(answer_raw)

    except Exception:
        return {
            "message": "Failed to parse LLM response",
            "raw_output": answer_raw
        }

    # =========================
    # OPTIONAL VALIDATION
    # =========================
    validation = verify_answer(
        answer_json.get("answer", ""),
        context
    )

    if not validation:
        answer_json = {
            "answer": "INVALID (not supported by book)",
            "evidence": ""
        }

    # =========================
    # SAVE TO DATABASE
    # =========================
    qa_entry = AskAI(
        id=str(uuid.uuid4()),
        user_id=user_id,
        book_id=book_id,
        question=question,
        answer=answer_json.get("answer", "")
    )

    db.add(qa_entry)
    db.commit()

    # =========================
    # FINAL RESPONSE
    # =========================
    return {
        "answer": answer_json.get("answer", ""),
        "evidence": answer_json.get("evidence", ""),
        "book_id": book_id,
        "user_id": user_id
    }
