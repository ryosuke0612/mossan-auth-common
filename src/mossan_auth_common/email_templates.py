"""Plain-text authentication email templates shared by all apps."""

from __future__ import annotations

from dataclasses import dataclass

from .policy import DEFAULT_AUTH_POLICY


@dataclass(frozen=True, slots=True)
class AuthEmail:
    subject: str
    text: str


def _required(value: str, label: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        raise ValueError(f"{label} is required")
    return cleaned


def _footer(*, app_name: str, support_contact: str) -> list[str]:
    lines: list[str] = []
    if support_contact.strip():
        lines.extend([f"お問い合わせ: {support_contact.strip()}", ""])
    lines.extend([app_name, "運営: Mossan Store"])
    return lines


def build_signup_confirmation_email(
    *,
    app_name: str,
    action_url: str,
    support_contact: str = "",
    expires_hours: int = DEFAULT_AUTH_POLICY.signup_confirmation_hours,
) -> AuthEmail:
    app_name = _required(app_name, "app_name")
    action_url = _required(action_url, "action_url")
    body = [
        f"{app_name} をご利用いただきありがとうございます。",
        "",
        "アカウント登録を受け付けました。",
        "以下のURLを開いて、メールアドレスの確認を完了してください。",
        "",
        action_url,
        "",
        f"このURLの有効期限は{expires_hours}時間です。",
        "このメールに心当たりがない場合は、操作せず破棄してください。",
        "",
        *_footer(app_name=app_name, support_contact=support_contact),
    ]
    return AuthEmail(subject=f"【{app_name}】メールアドレスの確認", text="\n".join(body))


def build_password_reset_email(
    *,
    app_name: str,
    action_url: str,
    support_contact: str = "",
    expires_hours: int = DEFAULT_AUTH_POLICY.password_reset_hours,
) -> AuthEmail:
    app_name = _required(app_name, "app_name")
    action_url = _required(action_url, "action_url")
    body = [
        f"{app_name} のパスワード再設定を受け付けました。",
        "",
        "以下のURLを開いて、新しいパスワードを設定してください。",
        "",
        action_url,
        "",
        f"このURLの有効期限は{expires_hours}時間です。",
        "このメールに心当たりがない場合は、操作せず破棄してください。",
        "",
        *_footer(app_name=app_name, support_contact=support_contact),
    ]
    return AuthEmail(subject=f"【{app_name}】パスワード再設定", text="\n".join(body))


def build_signup_completed_email(
    *, app_name: str, login_url: str, support_contact: str = ""
) -> AuthEmail:
    app_name = _required(app_name, "app_name")
    login_url = _required(login_url, "login_url")
    body = [
        f"{app_name} のアカウント登録が完了しました。",
        "",
        "以下のURLからログインできます。",
        login_url,
        "",
        *_footer(app_name=app_name, support_contact=support_contact),
    ]
    return AuthEmail(subject=f"【{app_name}】登録完了", text="\n".join(body))


def build_password_changed_email(*, app_name: str, support_contact: str = "") -> AuthEmail:
    app_name = _required(app_name, "app_name")
    body = [
        f"{app_name} のパスワードを変更しました。",
        "",
        "この変更に心当たりがない場合は、すぐにお問い合わせください。",
        "",
        *_footer(app_name=app_name, support_contact=support_contact),
    ]
    return AuthEmail(subject=f"【{app_name}】パスワード変更完了", text="\n".join(body))

