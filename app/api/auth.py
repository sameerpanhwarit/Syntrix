
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.core.auth import create_access_token
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


# =====================
# DB DEPENDENCY
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================
# REGISTER API (MISSING BEFORE)
# =====================
@router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):

    # check if user exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return {"message": "User already exists"}

    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User created successfully"
    }


# =====================
# LOGIN API
# =====================
# @router.post("/login")
# def login(email: str, password: str, db: Session = Depends(get_db)):
    
#     print(f"Credentials: {email} - {password}")
#     user = db.query(User).filter(User.email == email).first()

#     if not user or user.password != password:
#         return {"message": "Invalid credentials"}

#     token = create_access_token(user.id)

#     return {
#         "access_token": token,
#         "token_type": "bearer"
#     }

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or user.password != data.password:
        return {"message": "Invalid credentials"}

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }