"""Flask integration for the shared authentication pages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from flask import Blueprint, Flask, current_app, render_template


EXTENSION_KEY = "mossan_auth_common"


@dataclass(frozen=True, slots=True)
class AuthUIConfig:
    app_name: str
    logo_text: str
    logo_href: str
    login_url: str
    favicon_url: str = ""
    support_contact: str = ""


auth_ui_blueprint = Blueprint(
    "mossan_auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/assets",
)


def init_auth_ui(app: Flask, config: AuthUIConfig) -> None:
    """Register the common assets and store app-specific display settings."""

    if EXTENSION_KEY in app.extensions:
        raise RuntimeError("mossan-auth-common is already initialized")
    app.extensions[EXTENSION_KEY] = config
    app.register_blueprint(auth_ui_blueprint, url_prefix="/_mossan-auth")


def _config() -> AuthUIConfig:
    try:
        return current_app.extensions[EXTENSION_KEY]
    except KeyError as exc:
        raise RuntimeError("Call init_auth_ui(app, config) before rendering auth pages") from exc


def _render(template_name: str, **context: Any) -> str:
    return render_template(template_name, auth_ui=_config(), **context)


def render_login(
    *,
    form_action: str,
    forgot_password_url: str,
    error_message: str = "",
    info_message: str = "",
    next_value: str = "",
    email_value: str = "",
    remember_checked: bool = False,
    remember_field_name: str = "remember_admin",
) -> str:
    return _render(
        "mossan_auth/login.html",
        form_action=form_action,
        forgot_password_url=forgot_password_url,
        error_message=error_message,
        info_message=info_message,
        next_value=next_value,
        email_value=email_value,
        remember_checked=remember_checked,
        remember_field_name=remember_field_name,
    )


def render_password_forgot(
    *,
    form_action: str,
    error_message: str = "",
    info_message: str = "",
    email_value: str = "",
) -> str:
    return _render(
        "mossan_auth/password_forgot.html",
        form_action=form_action,
        error_message=error_message,
        info_message=info_message,
        email_value=email_value,
    )


def render_password_reset(
    *, form_action: str, error_message: str = "", info_message: str = ""
) -> str:
    return _render(
        "mossan_auth/password_reset.html",
        form_action=form_action,
        error_message=error_message,
        info_message=info_message,
    )

