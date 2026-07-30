"""
Short-code generation.

Uses a random alphanumeric string rather than an incrementing counter so
codes aren't guessable/enumerable (you shouldn't be able to find other
users' links by counting up from your own).
"""

import secrets
import string

_ALPHABET = string.ascii_letters + string.digits
_DEFAULT_LENGTH = 7


def generate_short_code(length: int = _DEFAULT_LENGTH) -> str:
    """Generate a random, URL-safe short code."""
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))
