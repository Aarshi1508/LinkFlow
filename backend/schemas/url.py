"""
Pydantic schemas for the URL resource.

Custom alias validation happens here at the API boundary (format/length),
while the "is this alias already taken" check is a DB concern handled in
services/url_service.py.
"""

import re
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator

# Allow letters, digits, hyphens, and underscores only - keeps short codes
# URL-safe without needing percent-encoding.
_ALIAS_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


class URLCreate(BaseModel):
    original_url: HttpUrl
    custom_alias: str | None = Field(default=None, min_length=3, max_length=20)

    @field_validator("custom_alias")
    @classmethod
    def validate_alias_format(cls, value: str | None) -> str | None:
        if value is not None and not _ALIAS_PATTERN.match(value):
            raise ValueError(
                "Alias may only contain letters, numbers, hyphens, and underscores."
            )
        return value


class URLUpdate(BaseModel):
    """All fields optional - a PUT here behaves as a partial update."""

    original_url: HttpUrl | None = None
    custom_alias: str | None = Field(default=None, min_length=3, max_length=20)

    @field_validator("custom_alias")
    @classmethod
    def validate_alias_format(cls, value: str | None) -> str | None:
        if value is not None and not _ALIAS_PATTERN.match(value):
            raise ValueError(
                "Alias may only contain letters, numbers, hyphens, and underscores."
            )
        return value


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    total_clicks: int
    last_visited: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
