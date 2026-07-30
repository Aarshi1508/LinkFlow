"""
Shared FastAPI dependencies used across routers.

`get_current_user` is the core of our auth system: any route that includes
it as a dependency automatically requires a valid Bearer token and gets the
authenticated User object injected as an argument.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.security import decode_access_token
from database.session import get_db
from models.user import User

# tokenUrl is only used for Swagger UI's "Authorize" button - it points at
# our login endpoint so the docs page can request a token interactively.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user
