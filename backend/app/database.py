"""
This file sets up the connection to PostgreSQL and gives us a way to
create/use database "sessions" (a session is basically a temporary
conversation with the database — open it, do some work, close it).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# The "engine" is the object that actually knows how to talk to PostgreSQL.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory that creates new database sessions when needed.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what our table models (User, Product, Sale) will inherit from.
Base = declarative_base()


def get_db():
    """
    This function is used by FastAPI to give each incoming request its own
    database session, and automatically close it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
