"""Shared authentication policy values and dependency-free helpers."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class AuthPolicy:
    password_min_length: int = 8
    signup_confirmation_hours: int = 24
    password_reset_hours: int = 1
    remember_session_days: int = 30
    login_rate_limit_window_seconds: int = 15 * 60
    login_rate_limit_max_attempts: int = 20
    signup_rate_limit_window_seconds: int = 60 * 60
    signup_rate_limit_max_attempts: int = 10
    password_reset_rate_limit_window_seconds: int = 60 * 60
    password_reset_rate_limit_max_attempts: int = 5


DEFAULT_AUTH_POLICY = AuthPolicy()


def normalize_email(value: str | None) -> str:
    """Normalize email input in the same way as the attendance app."""

    return (value or "").strip().lower()


def safe_next_path(value: str | None, fallback: str) -> str:
    """Return an app-local redirect path and reject external redirects."""

    raw_value = (value or "").strip()
    if not raw_value:
        return fallback
    parsed = urlsplit(raw_value)
    if parsed.scheme or parsed.netloc or not raw_value.startswith("/"):
        return fallback
    if raw_value.startswith("//"):
        return fallback
    return raw_value

