from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.ask_ai import AskAI
from app.models.assessment import Assessment

from app.core.deps import get_current_user


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/ask-history")
def get_ask_history(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = db.query(AskAI).filter(
        AskAI.user_id == user_id
    ).all()

    result = []

    for item in history:

        result.append({
            "question": item.question,
            "answer": item.answer,
            "book_id": item.book_id
        })

    return {
        "total": len(result),
        "history": result
    }

@router.get("/assessment-history")
def get_assessment_history(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = db.query(Assessment).filter(
        Assessment.user_id == user_id
    ).all()

    result = []

    for item in history:

        result.append({
            "assessment_id": item.id,
            "book_id": item.book_id,
            "score": item.score,
            "correct_answers": item.correct_answers,
            "total_questions": item.total_questions
        })

    return {
        "total": len(result),
        "history": result
    }