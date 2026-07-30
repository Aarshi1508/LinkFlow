"""
User ORM model.

Note: we store `password_hash`, never a plaintext password. This model has
no knowledge of JWT or hashing logic itself - that's handled in
core/security.py and services/auth_service.py. The model's only job is to
describe the shape of the `users` table.
"""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database.session import Base


class User(Base):
    __tablename__ = "users"

    # No explicit index=True here: a PRIMARY KEY already gets a unique
    # index from Postgres automatically - adding index=True on top of it
    # is redundant and was the root cause of a duplicate-index bug in the
    # initial Alembic migration (see alembic/versions/0001_initial_*.py).
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # One user can own many shortened URLs.
    # cascade="all, delete-orphan" -> deleting a user deletes their URLs too,
    # keeping the DB free of orphaned rows.
    urls: Mapped[list["URL"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
