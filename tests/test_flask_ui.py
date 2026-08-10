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
        self.assertIn("運営: Mossan Store", html)

    def test_common_stylesheet_is_served(self):
        with self.client.get("/_mossan-auth/assets/auth.css") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("--auth-primary", response.get_data(as_text=True))

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
