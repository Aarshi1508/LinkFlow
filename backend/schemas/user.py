"""
Pydantic schemas for the User resource.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

## Enforce bcrypt's 72-byte password limit before hashing.
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

     # Apply the same validation during login.
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
