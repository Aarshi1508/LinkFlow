"""
URL CRUD routes.

Every route here depends on get_current_user, so `current_user.id` is
always available and passed into the service layer for ownership checks.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from core.exceptions import ConflictError, ForbiddenError, NotFoundError
from database.session import get_db
from models.user import User
from schemas.url import URLCreate, URLResponse, URLUpdate
from services import url_service

router = APIRouter(tags=["URLs"])


@router.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(
    url_in: URLCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return url_service.create_url(db, current_user.id, url_in)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/urls", response_model=list[URLResponse])
def list_urls(
    search: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List the current user's URLs, optionally filtered by `?search=`."""
    return url_service.get_urls_for_user(db, current_user.id, search)


@router.get("/urls/{url_id}", response_model=URLResponse)
def get_url(
    url_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return url_service.get_url_by_id(db, url_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.put("/urls/{url_id}", response_model=URLResponse)
def edit_url(
    url_id: int,
    url_in: URLUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return url_service.update_url(db, url_id, current_user.id, url_in)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/urls/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_url(
    url_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        url_service.delete_url(db, url_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
