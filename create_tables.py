from app.db.database import Base, engine

from app.models.user import User
from app.models.book import Book
from app.models.ask_ai import AskAI
from app.models.assessment import Assessment

Base.metadata.create_all(bind=engine)

print("All tables created successfully")