"""
Importing all models here ensures that Alembic's `target_metadata` and any
`Base.metadata.create_all()` call sees every table - SQLAlchemy only
registers a model with the shared Base once its module has been imported.
"""

from models.user import User
from models.url import URL

__all__ = ["User", "URL"]
