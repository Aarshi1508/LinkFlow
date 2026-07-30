"""create users and urls tables

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-29

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Note: `id` columns are declared with primary_key=True only, no
    # index=True. A PRIMARY KEY constraint already creates a unique index
    # automatically in Postgres - adding index=True here would attach a
    # second, redundant Index object to the Table, which op.create_table
    # would then create *during* CREATE TABLE. A previous version of this
    # migration also had an explicit op.create_index("ix_users_id", ...)
    # call right after, which tried to create that same auto-generated
    # index a second time and crashed with DuplicateTable. Fixed by
    # removing index=True (no second index is needed) and removing the
    # now-unnecessary explicit create_index calls for id.
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "urls",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("original_url", sa.String(length=2048), nullable=False),
        sa.Column("short_code", sa.String(length=20), nullable=False),
        sa.Column("total_clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_visited", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_urls_short_code", "urls", ["short_code"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_urls_short_code", table_name="urls")
    op.drop_table("urls")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
