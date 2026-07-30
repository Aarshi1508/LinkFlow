"""
Auth routes: registration, login, and the current user's profile.

This router only handles HTTP concerns - parsing requests, calling the
service layer, and mapping exceptions to status codes. No DB queries or
password logic live here.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from core.exceptions import ConflictError, UnauthorizedError, ValidationAppError
from core.security import create_access_token
from database.session import get_db
from models.user import User
from schemas.user import Token, UserCreate, UserLogin, UserResponse
from services.auth_service import authenticate_user, register_user

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, user_in)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValidationAppError as e:
        # In normal operation, schemas.user.UserCreate's own byte-length
        # check on the password already rejects this before it ever
        # reaches register_user()/hash_password() - this catch is a
        # defense-in-depth backstop, not the primary mechanism.
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, credentials.email, credentials.password)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except ValidationAppError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    access_token = create_access_token(subject=str(user.id))
    return Token(access_token=access_token)


@router.get("/profile", response_model=UserResponse)
def profile(current_user: User = Depends(get_current_user)):
    """Returns the currently authenticated user's profile."""
    return current_user
