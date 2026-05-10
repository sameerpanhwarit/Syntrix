import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.sql import func

from app.db.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    # Book info
    title = Column(String, nullable=False)

    file_path = Column(String, nullable=False)

    # 📦 NEW FIELDS

    file_size_kb = Column(Integer, nullable=True)   # book size in KB

    total_pages = Column(Integer, nullable=True)    # optional later

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )