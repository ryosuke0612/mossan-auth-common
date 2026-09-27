"""Flask integration for the shared authentication pages."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from flask import Blueprint, Flask, current_app, render_template


EXTENSION_KEY = "mossan_auth_common"
_VALID_LOGO_VARIANTS = frozenset({"handwritten", "product"})
_HEX_COLOR_PATTERN = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{5})?\Z")


@dataclass(frozen=True, slots=True)
class AuthUIConfig:
    app_name: str
    logo_text: str
    logo_href: str
    login_url: str
    favicon_url: str = ""
    support_contact: str = ""
    logo_variant: str = "handwritten"
    logo_main_text: str = ""
    logo_suffix_text: str = ""
    logo_accent_color: str = ""

    def __post_init__(self) -> None:
        if self.logo_variant not in _VALID_LOGO_VARIANTS:
            raise ValueError(f"Unsupported logo_variant: {self.logo_variant}")
        if self.logo_suffix_text and not self.logo_main_text:
            raise ValueError("logo_main_text is required when logo_suffix_text is set")
        if self.logo_accent_color:
            if not self.logo_suffix_text:
                raise ValueError("logo_suffix_text is required when logo_accent_color is set")
            if not _HEX_COLOR_PATTERN.fullmatch(self.logo_accent_color):
                raise ValueError("logo_accent_color must be a 3, 6, or 8 digit hex color")


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


def _required_csrf_token(csrf_token: str) -> str:
    if not isinstance(csrf_token, str) or not csrf_token.strip():
        raise ValueError("csrf_token is required for authentication forms")
    return csrf_token


def render_login(
    *,
    csrf_token: str,
    form_action: str,
    forgot_password_url: str,
    error_message: str = "",
    info_message: str = "",
    login_helper_message: str = "",
    next_value: str = "",
    email_value: str = "",
    remember_checked: bool = False,
    remember_field_name: str = "remember_admin",
) -> str:
    return _render(
        "mossan_auth/login.html",
        csrf_token=_required_csrf_token(csrf_token),
        form_action=form_action,
        forgot_password_url=forgot_password_url,
        error_message=error_message,
        info_message=info_message,
        login_helper_message=login_helper_message,
        next_value=next_value,
        email_value=email_value,
        remember_checked=remember_checked,
        remember_field_name=remember_field_name,
    )


def render_password_forgot(
    *,
    csrf_token: str,
    form_action: str,
    error_message: str = "",
    info_message: str = "",
    email_value: str = "",
) -> str:
    return _render(
        "mossan_auth/password_forgot.html",
        csrf_token=_required_csrf_token(csrf_token),
        form_action=form_action,
        error_message=error_message,
        info_message=info_message,
        email_value=email_value,
    )


def render_password_reset(
    *,
    csrf_token: str,
    form_action: str,
    forgot_password_url: str = "",
    error_message: str = "",
    info_message: str = "",
) -> str:
    return _render(
        "mossan_auth/password_reset.html",
        csrf_token=_required_csrf_token(csrf_token),
        form_action=form_action,
        forgot_password_url=forgot_password_url,
        error_message=error_message,
        info_message=info_message,
    )
