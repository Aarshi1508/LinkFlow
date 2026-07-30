"""
URL ORM model - represents a single shortened link.

`short_code` is unique and indexed since it's the lookup key on every
redirect request (GET /link/{shortCode}) - this needs to be fast.
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database.session import Base


class URL(Base):
    __tablename__ = "urls"

    # Primary keys are indexed automatically by PostgreSQL.
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    short_code: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)

    total_clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_visited: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner: Mapped["User"] = relationship(back_populates="urls")
