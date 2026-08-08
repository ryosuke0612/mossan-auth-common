import unittest

from flask import Flask

from mossan_auth_common.flask_ui import AuthUIConfig, init_auth_ui, render_login


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
                form_action="/admin/login",
                forgot_password_url="/admin/password/forgot",
                info_message="テスト案内",
                next_value="/dashboard",
            )

        self.client = app.test_client()

    def test_login_page_uses_app_brand_and_common_fields(self):
        with self.client.get("/admin/login") as response:
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
        self.assertIn("<title>管理者ログイン | KYP</title>", html)
        self.assertIn('name="email"', html)
        self.assertIn('name="password"', html)
        self.assertIn('name="remember_admin"', html)
        self.assertIn('value="/dashboard"', html)
        self.assertIn("運営: Mossan Store", html)

    def test_common_stylesheet_is_served(self):
        with self.client.get("/_mossan-auth/assets/auth.css") as response:
            self.assertEqual(response.status_code, 200)
            self.assertIn("--auth-primary", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
