import uuid
from sqlalchemy import Column, String, ForeignKey, Text
from app.db.database import Base


class AskAI(Base):
    __tablename__ = "ask_ai"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    book_id = Column(String, ForeignKey("books.id"), nullable=False)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)