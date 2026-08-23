"""
Handles turning a plain password into a scrambled (hashed) version for
storage, and checking a plain password against a stored hash at login time.
We use bcrypt, a well-tested hashing algorithm designed specifically for
passwords (it's intentionally slow, which makes brute-force attacks harder).
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
