"""
Dashboard route: aggregate stats for the authenticated user.

Not in the original spec's endpoint list explicitly, but required by the
"Dashboard" feature (total links, total clicks, active links) - added as
GET /dashboard/stats rather than folding it into GET /urls, since it's a
different shape of data (aggregates, not a list) and the frontend dashboard
page will want to fetch it independently of the URL list/table.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_current_user
from database.session import get_db
from models.user import User
from schemas.dashboard import DashboardStats
from services import url_service

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard/stats", response_model=DashboardStats)
def dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stats = url_service.get_dashboard_stats(db, current_user.id)
    return DashboardStats(**stats)
