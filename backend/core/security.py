"""
Security primitives: password hashing and JWT creation/verification.

Kept separate from business logic (services/) because these are pure,
reusable, security-critical utilities with no knowledge of "users" or "urls" -
they just deal with strings, hashes, and tokens.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from core.config import settings
from core.exceptions import ValidationAppError

# bcrypt is the industry-standard choice for password hashing: it's slow by
# design (resists brute force) and has a built-in per-hash salt.
#
# We call the `bcrypt` library directly rather than going through passlib's
# CryptContext. passlib (last released in 2020, effectively unmaintained)
# detects the installed bcrypt backend's version by reading
# `bcrypt.__about__.__version__`; modern bcrypt (4.1+) removed that
# submodule entirely, so passlib crashes with
# `AttributeError: module 'bcrypt' has no attribute '__about__'` on the
# very first hash/verify call. Calling `bcrypt` directly sidesteps that
# broken version-sniffing code path completely, works with any current
# bcrypt release, and needs no extra dependency for a single hashing
# scheme like this project uses.

# bcrypt's underlying algorithm silently ignores any bytes past the 72nd -
# current bcrypt releases raise ValueError instead of truncating silently,
# which is safer but must be turned into a proper validation error before
# it ever reaches bcrypt, not left to crash as an unhandled 500.
BCRYPT_MAX_PASSWORD_BYTES = 72


def _check_password_length(plain_password: str) -> None:
    """
    Raise a clear, catchable error for passwords bcrypt cannot hash.

    Deliberately checks byte length (UTF-8 encoded), not character/string
    length - a handful of multi-byte characters (e.g. emoji, many non-Latin
    scripts) can exceed 72 bytes well before the string "looks" long, so a
    plain `len(password) > 72` check would under-count and still crash.
    """
    if len(plain_password.encode("utf-8")) > BCRYPT_MAX_PASSWORD_BYTES:
        raise ValidationAppError(
            f"Password is too long: it must be at most "
            f"{BCRYPT_MAX_PASSWORD_BYTES} bytes when UTF-8 encoded "
            f"(most passwords using only standard keyboard characters are "
            f"fine up to {BCRYPT_MAX_PASSWORD_BYTES} characters)."
        )


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password for storage."""
    # This check is also enforced at the API boundary in
    # schemas/user.py (so a bad request never even reaches this function
    # in normal operation) - it's repeated here as defense-in-depth, since
    # hash_password() could in principle be called from other code paths
    # (a script, a future admin tool) that don't go through that schema.
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

    `subject` is the value we want to identify the user by later - we use the
    user's id (as a string) so routers can look them up without a DB hit
    keyed on anything guessable.
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
