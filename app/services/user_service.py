from sqlalchemy.orm import Session
from app import crud
from app.schemas import user as user_schema

def create_user(db: Session, user_in: user_schema.UserCreate):
    existing = crud.user.get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")
    return crud.user.create_user(db, user_in)