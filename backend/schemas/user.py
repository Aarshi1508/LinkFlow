"""
Pydantic schemas for the User resource.

Kept separate from models/user.py on purpose: these define the API contract
(what clients send/receive), while the SQLAlchemy model defines the DB
table. UserResponse deliberately excludes password_hash - it should never
leave the server.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

# bcrypt (see core/security.py) can only hash the first 72 bytes of a
# password - anything beyond that is either silently ignored or (in
# current bcrypt releases) raises an error. Rejecting an over-length
# password here, at the API boundary, means the request fails with a
# clear 422 instead of a 500 from deep inside the hashing/verification
# call. Checked as UTF-8 byte length, not character count, since a
# handful of multi-byte characters (emoji, many non-Latin scripts) can
# exceed 72 bytes well before the string "looks" long.
_BCRYPT_MAX_PASSWORD_BYTES = 72


def _validate_bcrypt_length(value: str) -> str:
    if len(value.encode("utf-8")) > _BCRYPT_MAX_PASSWORD_BYTES:
        raise ValueError(
            f"Password is too long: it must be at most "
            f"{_BCRYPT_MAX_PASSWORD_BYTES} bytes when UTF-8 encoded "
            f"(most passwords using only standard keyboard characters are "
            f"fine up to {_BCRYPT_MAX_PASSWORD_BYTES} characters)."
        )
    return value


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    _validate_password_length = field_validator("password")(_validate_bcrypt_length)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    # Same check as UserCreate: without this, a login attempt with a very
    # long password would reach bcrypt's verify call directly and crash
    # with a 500 instead of failing cleanly.
    _validate_password_length = field_validator("password")(_validate_bcrypt_length)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    # Allows creating this schema directly from a SQLAlchemy model instance
    # (model.id, model.name, etc.) instead of manually building a dict.
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
