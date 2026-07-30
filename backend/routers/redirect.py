"""
Public redirect route.

Deliberately has NO auth dependency - anyone with a short link should be
able to use it, that's the entire point of a URL shortener. Click tracking
(increment count + update last_visited) happens here, right before the
redirect, so every real visit is counted exactly once.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from core.exceptions import NotFoundError
from database.session import get_db
from services import url_service

router = APIRouter(tags=["Redirect"])


@router.get("/link/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    try:
        url = url_service.get_url_by_short_code(db, short_code)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    url_service.record_click(db, url)

    # 307 preserves the original request method (harmless here since this is
    # always a GET, but it's the more correct choice than a 301/302 for a
    # redirect that isn't meant to be permanently cached by browsers - click
    # counts would otherwise stop being recorded after the first visit.
    return RedirectResponse(url=url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
