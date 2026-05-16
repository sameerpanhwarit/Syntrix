
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

import json
import uuid

from app.db.database import SessionLocal

from app.models.book import Book
from app.models.assessment import Assessment

from app.core.deps import get_current_user
from app.core.llm import call_llm

from app.services.embeddings import get_embeddings
from app.services.rag import search


router = APIRouter()


class MCQRequest(BaseModel):
    book_id: str
    number_of_questions: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate-mcqs")
def generate_mcqs(
    data: MCQRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    book_id = data.book_id
    number_of_questions = data.number_of_questions

    book = db.query(Book).filter(
        Book.id == book_id,
        Book.user_id == user_id
    ).first()

    if not book:
        return {
            "message": "Unauthorized or book not found"
        }


    query_embedding = get_embeddings(
        ["Generate MCQs from this book"]
    )[0]

    results = search(
        query_embedding,
        book_id=book_id,
        k=10
    )

    if not results:
        return {
            "message": "No relevant content found in this book"
        }


    chunks = [r["text"] for r in results]

    context = "\n\n".join(chunks)

    prompt = f"""
You are a strict AI exam generator.

Generate EXACTLY {number_of_questions} MCQs ONLY from the provided context.

Return ONLY valid JSON.

FORMAT:

{{
  "mcqs": [
    {{
      "question": "question here",
      "options": {{
        "A": "option A",
        "B": "option B",
        "C": "option C",
        "D": "option D"
      }},
      "correct_answer": "A"
    }}
  ]
}}

RULES:
- Use ONLY the provided context
- Do NOT use external knowledge
- Do NOT explain anything
- No markdown
- No extra text
- Return valid JSON ONLY

Context:
{context}
"""

    # ====================================
    # CALL LLM
    # ====================================
    response_raw = call_llm(prompt)

    # ====================================
    # SAFE JSON PARSING
    # ====================================
    try:
        response_json = json.loads(response_raw)

    except Exception:
        return {
            "message": "Failed to parse MCQs",
            "raw_response": response_raw
        }

    # ====================================
    # VALIDATE MCQ STRUCTURE
    # ====================================
    mcqs = response_json.get("mcqs", [])

    if not mcqs:
        return {
            "message": "No MCQs generated"
        }

    # ====================================
    # SAVE ASSESSMENT SESSION
    # ====================================
    assessment = Assessment(
        id=str(uuid.uuid4()),
        user_id=user_id,
        book_id=book_id,
        total_questions=len(mcqs),
        correct_answers=0,
        score=0
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    # ====================================
    # FINAL RESPONSE
    # ====================================
    return {
        "assessment_id": assessment.id,
        "book_id": book_id,
        "user_id": user_id,
        "total_questions": len(mcqs),
        "mcqs": mcqs
    }

