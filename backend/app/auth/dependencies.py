"""
This is a FastAPI "dependency" — a function that other endpoints can plug
in to automatically require login. Any endpoint that includes
`current_user: User = Depends(get_current_user)` will:
  1. Read the JWT from the Authorization header
  2. Decode and verify it
  3. Look up the matching user in the database
  4. Reject the request with 401 Unauthorized if any step fails

This is how we make sure a user can only see and modify their own data.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.auth.jwt_handler import decode_access_token

# This tells FastAPI where the frontend should send login requests to get
# a token (used for the automatic API docs page, /docs).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user
