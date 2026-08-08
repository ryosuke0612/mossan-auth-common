"""Mossan Store shared authentication contracts."""

from .email_templates import (
    AuthEmail,
    build_password_changed_email,
    build_password_reset_email,
    build_signup_completed_email,
    build_signup_confirmation_email,
)
from .policy import DEFAULT_AUTH_POLICY, AuthPolicy, normalize_email, safe_next_path
from .schema import AUTH_SCHEMA_VERSION, auth_schema

__all__ = [
    "AUTH_SCHEMA_VERSION",
    "DEFAULT_AUTH_POLICY",
    "AuthEmail",
    "AuthPolicy",
    "auth_schema",
    "build_password_changed_email",
    "build_password_reset_email",
    "build_signup_completed_email",
    "build_signup_confirmation_email",
    "normalize_email",
    "safe_next_path",
]

