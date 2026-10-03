import unittest

from flask import Flask

from mossan_auth_common.flask_ui import (
    AuthUIConfig,
    init_auth_ui,
    render_login,
    render_password_forgot,
    render_password_reset,
)


class FlaskUITests(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config.update(TESTING=True, SECRET_KEY="test-only")
        init_auth_ui(
            app,
            AuthUIConfig(
                app_name="KYP",
                logo_text="KYP",
                logo_href="https://example.com/kyp",
                login_url="/admin/login",
            ),
        )

        @app.get("/admin/login")
        def login_page():
            return render_login(
                csrf_token="test-csrf-token",
                form_action="/admin/login",
                forgot_password_url="/admin/password/forgot",
                info_message="テスト案内",
                login_helper_message="初めてご利用の場合の案内",
                next_value="/dashboard",
            )

        @app.get("/admin/password/forgot")
        def password_forgot_page():
            return render_password_forgot(
                csrf_token="test-forgot-csrf-token",
                form_action="/admin/password/forgot",
            )

        @app.get("/admin/password/reset/<token>")
        def password_reset_page(token):
            return render_password_reset(
                csrf_token="test-reset-csrf-token",
                form_action=f"/admin/password/reset/{token}",
                forgot_password_url="/admin/password/forgot",
            )

        self.client = app.test_client()
        self.app = app

    def test_login_page_uses_app_brand_and_common_fields(self):
        with self.client.get("/admin/login") as response:
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
        self.assertIn("<title>管理者ログイン | KYP</title>", html)
        self.assertIn('name="email"', html)
        self.assertIn('name="password"', html)
        self.assertIn('name="remember_admin"', html)
        self.assertIn('name="csrf_token" value="test-csrf-token"', html)
        self.assertIn('value="/dashboard"', html)
        self.assertIn('class="auth-logo__text">KYP</span>', html)
        self.assertIn('class="auth-form auth-login-form"', html)
        self.assertIn("初めてご利用の場合の案内", html)
        self.assertIn(">ログイン</button>", html)
        self.assertIn("ログイン状態を保持する", html)
        self.assertNotIn("管理者としてログイン", html)
        self.assertIn('<nav class="auth-nav"', html)
        self.assertIn(
            'href="https://mossan-store.com/contact/">お問い合わせ</a>',
            html,
        )
        self.assertNotIn('href="/admin/login">管理者ログイン</a>', html)
        self.assertIn("<svg", html)
        self.assertNotIn("運営: Mossan Store", html)

    def test_common_stylesheet_is_served(self):
        with self.client.get("/_mossan-auth/assets/auth.css") as response:
            self.assertEqual(response.status_code, 200)
            css = response.get_data(as_text=True)
            self.assertIn("color-scheme: dark", css)
            self.assertIn("radial-gradient", css)
            self.assertIn("#1b1012", css)
            self.assertIn("width: min(510px, 100%)", css)
            self.assertIn(".auth-logo__text--product", css)

    def test_product_logo_can_keep_app_specific_typography(self):
        app = Flask(__name__)
        app.config.update(TESTING=True, SECRET_KEY="test-only")
        init_auth_ui(
            app,
            AuthUIConfig(
                app_name="LightSketch+",
                logo_text="LightSketch+",
                logo_href="https://example.com/lightsketch",
                login_url="/login",
                logo_variant="product",
                logo_main_text="LightSketch",
                logo_suffix_text="+",
                logo_accent_color="#ff8a00",
            ),
        )

        @app.get("/login")
        def login_page():
            return render_login(
                csrf_token="test-csrf-token",
                form_action="/login",
                forgot_password_url="/password/forgot",
            )

        with app.test_client().get("/login") as response:
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
        self.assertIn('auth-logo__text--product', html)
        self.assertIn('style="--auth-logo-accent: #ff8a00;"', html)
        self.assertIn('<span class="auth-logo__main">LightSketch</span>', html)
        self.assertIn('<span class="auth-logo__suffix">+</span>', html)

    def test_invalid_product_logo_settings_are_rejected(self):
        base_config = {
            "app_name": "Example",
            "logo_text": "Example",
            "logo_href": "https://example.com/",
            "login_url": "/login",
        }
        with self.assertRaisesRegex(ValueError, "Unsupported logo_variant"):
            AuthUIConfig(**base_config, logo_variant="application-name")
        with self.assertRaisesRegex(ValueError, "logo_main_text is required"):
            AuthUIConfig(**base_config, logo_suffix_text="+")
        with self.assertRaisesRegex(ValueError, "3, 6, or 8 digit hex color"):
            AuthUIConfig(
                **base_config,
                logo_main_text="Example",
                logo_suffix_text="+",
                logo_accent_color="orange",
            )

    def test_password_forms_include_their_csrf_token(self):
        cases = (
            ("/admin/password/forgot", "test-forgot-csrf-token"),
            ("/admin/password/reset/test-token", "test-reset-csrf-token"),
        )
        for path, token in cases:
            with self.subTest(path=path):
                with self.client.get(path) as response:
                    self.assertEqual(response.status_code, 200)
                    html = response.get_data(as_text=True)
                self.assertIn(f'name="csrf_token" value="{token}"', html)

    def test_password_reset_can_link_back_to_resend_email(self):
        with self.client.get("/admin/password/reset/test-token") as response:
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
        self.assertIn('href="/admin/password/forgot">メールを再送する</a>', html)

    def test_all_auth_forms_require_a_csrf_token(self):
        renderers = (
            lambda: render_login(
                csrf_token="",
                form_action="/admin/login",
                forgot_password_url="/admin/password/forgot",
            ),
            lambda: render_password_forgot(
                csrf_token="",
                form_action="/admin/password/forgot",
            ),
            lambda: render_password_reset(
                csrf_token="",
                form_action="/admin/password/reset/token",
            ),
        )
        with self.app.test_request_context():
            for render_form in renderers:
                with self.subTest(render_form=render_form):
                    with self.assertRaisesRegex(ValueError, "csrf_token is required"):
                        render_form()


if __name__ == "__main__":
    unittest.main()
