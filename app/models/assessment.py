import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from app.db.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    book_id = Column(String, ForeignKey("books.id"), nullable=False)

    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    score = Column(Float)