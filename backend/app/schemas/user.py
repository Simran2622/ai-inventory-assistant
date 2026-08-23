"""
These are "schemas" — they are NOT database tables. They just describe
what shape of data we expect to receive from the frontend, and what shape
of data we send back. FastAPI uses these to automatically validate input
(e.g., reject a request if "email" is missing or not a valid email) and to
make sure we never accidentally send back sensitive fields like passwords.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # allows converting a SQLAlchemy object directly


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
