"""
This is the entry point of the backend. Running this file starts the
FastAPI server. It:
  1. Creates database tables if they don't exist yet
  2. Allows the frontend (running on a different domain, e.g. Netlify) to
     make requests to this backend (CORS)
  3. Registers our endpoints (/auth/*, /products/*, /products/{id}/sales/*,
     /dashboard/*)
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, products, sales, dashboard
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserOut

# Creates all tables defined by our models (users, products, sales)
# if they don't already exist in the database.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Inventory & Demand Assistant")

# CORS: without this, a browser will block the frontend (on a different
# domain) from calling this API. For now we allow all origins to keep
# local development simple — we will restrict this before deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"status": "AI Inventory & Demand Assistant API is running"}


@app.get("/auth/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    """A simple protected endpoint — useful to test that JWT auth works."""
    return current_user