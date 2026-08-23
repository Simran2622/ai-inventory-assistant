"""
Handles creating and reading JWTs (JSON Web Tokens).

A JWT is a signed piece of text that encodes some data (in our case, the
user's email) plus an expiry time. It's "signed" using our SECRET_KEY, so
if anyone tries to tamper with it, the signature won't match anymore and
we'll reject it. This lets the server verify "who is this?" without
storing any session data.
"""

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

ALGORITHM = "HS256"


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
