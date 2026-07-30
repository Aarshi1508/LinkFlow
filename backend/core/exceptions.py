"""
Custom application exceptions.

Services raise these instead of HTTPException directly - services shouldn't
know about HTTP status codes (that's a web-layer concern). Routers catch
these and translate them to the correct HTTP response. This keeps services
reusable outside of a web context (e.g. in a CLI script or test suite).
"""


class AppError(Exception):
    """Base class for all application-level errors."""


class NotFoundError(AppError):
    """Raised when a requested resource doesn't exist."""


class ConflictError(AppError):
    """Raised when a resource already exists (e.g. duplicate email/alias)."""


class UnauthorizedError(AppError):
    """Raised when credentials are invalid or a token can't be verified."""


class ForbiddenError(AppError):
    """Raised when a user tries to act on a resource they don't own."""


class ValidationAppError(AppError):
    """Raised for domain-level validation failures beyond Pydantic's scope."""
