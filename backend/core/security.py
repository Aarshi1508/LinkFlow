"""
Security primitives: password hashing and JWT creation/verification.

"""

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from core.config import settings
from core.exceptions import ValidationAppError

# Use bcrypt directly instead of passlib to avoid compatibility issues with
# newer bcrypt releases.
BCRYPT_MAX_PASSWORD_BYTES = 72


def _check_password_length(plain_password: str) -> None:
 
    if len(plain_password.encode("utf-8")) > BCRYPT_MAX_PASSWORD_BYTES:
        raise ValidationAppError(
            f"Password is too long: it must be at most "
            f"{BCRYPT_MAX_PASSWORD_BYTES} bytes when UTF-8 encoded "
            f"(most passwords using only standard keyboard characters are "
            f"fine up to {BCRYPT_MAX_PASSWORD_BYTES} characters)."
        )


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password for storage."""

    _check_password_length(plain_password)
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against a stored bcrypt hash."""
    _check_password_length(plain_password)
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """
    Create a signed JWT.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """
    Decode and validate a JWT, returning the subject (user id) if valid,
    or None if the token is invalid/expired.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
