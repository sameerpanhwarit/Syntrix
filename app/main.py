from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.upload import router as upload_router
from app.api.qa import router as qa_router
from app.api.mcq import router as mcq_router
from app.api.test import router as test_router
from app.api.books import router as books_router
from app.api.history import router as history_router
from app.api.delete_book import router as delete_book_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(qa_router)
app.include_router(mcq_router)
app.include_router(test_router)
app.include_router(books_router)
app.include_router(history_router)
app.include_router(delete_book_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)