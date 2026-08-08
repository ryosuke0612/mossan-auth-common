"""Logical authentication schema shared across separate app databases."""

from __future__ import annotations

from dataclasses import dataclass


AUTH_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class ColumnSpec:
    name: str
    nullable: bool
    unique: bool = False
    references: str | None = None


@dataclass(frozen=True, slots=True)
class TableSpec:
    name: str
    columns: tuple[ColumnSpec, ...]
    indexes: tuple[tuple[str, ...], ...] = ()


def auth_schema() -> tuple[TableSpec, ...]:
    """Return the database-independent authentication schema contract."""

    return (
        TableSpec(
            name="admins",
            columns=(
                ColumnSpec("id", nullable=False, unique=True),
                ColumnSpec("common_user_id", nullable=True, unique=True),
                ColumnSpec("email", nullable=False, unique=True),
                ColumnSpec("password_hash", nullable=False),
                ColumnSpec("account_status", nullable=False),
                ColumnSpec("email_confirmed_at", nullable=True),
                ColumnSpec("created_at", nullable=False),
                ColumnSpec("updated_at", nullable=False),
                ColumnSpec("last_login_at", nullable=True),
                ColumnSpec("password_changed_at", nullable=True),
            ),
            indexes=(("email",), ("common_user_id",)),
        ),
        TableSpec(
            name="pending_admin_signups",
            columns=(
                ColumnSpec("id", nullable=False, unique=True),
                ColumnSpec("email", nullable=False),
                ColumnSpec("password_hash", nullable=False),
                ColumnSpec("token_hash", nullable=False, unique=True),
                ColumnSpec("created_at", nullable=False),
                ColumnSpec("expires_at", nullable=False),
                ColumnSpec("used_at", nullable=True),
                ColumnSpec("remote_addr", nullable=True),
                ColumnSpec("user_agent", nullable=True),
            ),
            indexes=(("email",), ("token_hash",)),
        ),
        TableSpec(
            name="admin_password_reset_tokens",
            columns=(
                ColumnSpec("id", nullable=False, unique=True),
                ColumnSpec("admin_id", nullable=False, references="admins.id"),
                ColumnSpec("token_hash", nullable=False, unique=True),
                ColumnSpec("created_at", nullable=False),
                ColumnSpec("expires_at", nullable=False),
                ColumnSpec("used_at", nullable=True),
                ColumnSpec("remote_addr", nullable=True),
                ColumnSpec("user_agent", nullable=True),
            ),
            indexes=(("admin_id",), ("token_hash",)),
        ),
    )

