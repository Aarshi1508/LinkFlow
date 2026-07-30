"""
URL business logic: creating, listing, searching, updating, and deleting
shortened links, plus recording clicks on redirect.

Ownership enforcement lives here: every read/update/delete takes the
requesting user's id and raises ForbiddenError/NotFoundError as
appropriate, so routers never have to remember to check ownership
themselves.
"""

from datetime import datetime, timezone

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from core.exceptions import ConflictError, ForbiddenError, NotFoundError
from models.url import URL
from schemas.url import URLCreate, URLUpdate
from utils.short_code import generate_short_code

_MAX_ALIAS_RETRIES = 5


def _code_exists(db: Session, code: str) -> bool:
    return db.query(URL).filter(URL.short_code == code).first() is not None


def create_url(db: Session, user_id: int, url_in: URLCreate) -> URL:
    """Create a shortened URL, using a custom alias if provided."""
    if url_in.custom_alias:
        if _code_exists(db, url_in.custom_alias):
            raise ConflictError(f"Alias '{url_in.custom_alias}' is already taken.")
        short_code = url_in.custom_alias
    else:
        # Retry a handful of times on the (very unlikely) chance of a
        # collision with an existing random code.
        for _ in range(_MAX_ALIAS_RETRIES):
            candidate = generate_short_code()
            if not _code_exists(db, candidate):
                short_code = candidate
                break
        else:
            raise ConflictError("Could not generate a unique short code, please retry.")

    url = URL(
        user_id=user_id,
        original_url=str(url_in.original_url),
        short_code=short_code,
    )
    db.add(url)
    db.commit()
    db.refresh(url)
    return url


def get_urls_for_user(db: Session, user_id: int, search: str | None = None) -> list[URL]:
    """List a user's URLs, optionally filtered by a search term on the
    original URL or short code."""
    query = db.query(URL).filter(URL.user_id == user_id)
    if search:
        like_term = f"%{search}%"
        query = query.filter(
            or_(URL.original_url.ilike(like_term), URL.short_code.ilike(like_term))
        )
    return query.order_by(URL.created_at.desc()).all()


def _get_owned_url_or_raise(db: Session, url_id: int, user_id: int) -> URL:
    url = db.query(URL).filter(URL.id == url_id).first()
    if url is None:
        raise NotFoundError("URL not found.")
    if url.user_id != user_id:
        raise ForbiddenError("You do not have access to this URL.")
    return url


def get_url_by_id(db: Session, url_id: int, user_id: int) -> URL:
    return _get_owned_url_or_raise(db, url_id, user_id)


def update_url(db: Session, url_id: int, user_id: int, url_in: URLUpdate) -> URL:
    url = _get_owned_url_or_raise(db, url_id, user_id)

    if url_in.original_url is not None:
        url.original_url = str(url_in.original_url)

    if url_in.custom_alias is not None and url_in.custom_alias != url.short_code:
        if _code_exists(db, url_in.custom_alias):
            raise ConflictError(f"Alias '{url_in.custom_alias}' is already taken.")
        url.short_code = url_in.custom_alias

    db.commit()
    db.refresh(url)
    return url


def delete_url(db: Session, url_id: int, user_id: int) -> None:
    url = _get_owned_url_or_raise(db, url_id, user_id)
    db.delete(url)
    db.commit()


def get_url_by_short_code(db: Session, short_code: str) -> URL:
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url is None:
        raise NotFoundError("Short link not found.")
    return url


def record_click(db: Session, url: URL) -> None:
    """Increment click count and update last_visited on redirect."""
    url.total_clicks = URL.total_clicks + 1
    url.last_visited = datetime.now(timezone.utc)
    db.commit()


def get_dashboard_stats(db: Session, user_id: int) -> dict:
    """Aggregate stats for the dashboard: total links, total clicks, active links."""
    total_links = db.query(func.count(URL.id)).filter(URL.user_id == user_id).scalar()
    total_clicks = (
        db.query(func.coalesce(func.sum(URL.total_clicks), 0))
        .filter(URL.user_id == user_id)
        .scalar()
    )
    # "Active" = has received at least one click.
    active_links = (
        db.query(func.count(URL.id))
        .filter(URL.user_id == user_id, URL.total_clicks > 0)
        .scalar()
    )
    return {
        "total_links": total_links,
        "total_clicks": int(total_clicks),
        "active_links": active_links,
    }
