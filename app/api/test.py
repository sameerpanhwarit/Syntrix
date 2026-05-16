from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.assessment import Assessment

from app.core.deps import get_current_user


router = APIRouter()

class AnswerItem(BaseModel):
    question: str
    selected_answer: str
    correct_answer: str


class SubmitTestRequest(BaseModel):
    assessment_id: str
    answers: list[AnswerItem]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/submit-test")
def submit_test(
    data: SubmitTestRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    assessment = db.query(Assessment).filter(
        Assessment.id == data.assessment_id,
        Assessment.user_id == user_id
    ).first()

    if not assessment:
        return {
            "message": "Assessment not found or unauthorized"
        }


    correct_count = 0

    results = []

    for item in data.answers:

        is_correct = (
            item.selected_answer.strip().upper()
            ==
            item.correct_answer.strip().upper()
        )

        if is_correct:
            correct_count += 1

        results.append({
            "question": item.question,
            "selected_answer": item.selected_answer,
            "correct_answer": item.correct_answer,
            "is_correct": is_correct
        })

    total_questions = len(data.answers)

    score = 0

    if total_questions > 0:
        score = round(
            (correct_count / total_questions) * 100,
            2
        )


    assessment.correct_answers = correct_count
    assessment.score = score

    db.commit()

    return {
        "assessment_id": assessment.id,
        "user_id": user_id,
        "score": score,
        "correct_answers": correct_count,
        "wrong_answers": total_questions - correct_count,
        "total_questions": total_questions,
        "results": results
    }