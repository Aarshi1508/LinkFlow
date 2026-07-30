"""Pydantic schema for the dashboard summary endpoint."""

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_links: int
    total_clicks: int
    active_links: int
