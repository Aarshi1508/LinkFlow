"""
Auth business logic: registering users and verifying login credentials.

Routers call these functions and translate the exceptions raised here into
HTTP responses - this file has no knowledge of FastAPI or HTTP.
"""

from sqlalchemy.orm import Session

from core.exceptions import ConflictError, UnauthorizedError
from core.security import hash_password, verify_password
from models.user import User
from schemas.user import UserCreate


def register_user(db: Session, user_in: UserCreate) -> User:
    """Create a new user, hashing their password before storage."""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise ConflictError("A user with this email already exists.")

    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Verify email/password and return the User if valid, else raise."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        # Deliberately vague: don't reveal whether the email exists or the
        # password was wrong - avoids leaking which emails are registered.
        raise UnauthorizedError("Invalid email or password.")
    return user
