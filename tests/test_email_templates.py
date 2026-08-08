import unittest

from mossan_auth_common.email_templates import (
    build_password_reset_email,
    build_signup_confirmation_email,
)


class EmailTemplateTests(unittest.TestCase):
    def test_signup_subject_is_short_and_app_first(self):
        email = build_signup_confirmation_email(
            app_name="出欠ボード＋",
            action_url="https://example.com/confirm/token",
            support_contact="support@example.com",
        )
        self.assertEqual(email.subject, "【出欠ボード＋】メールアドレスの確認")
        self.assertNotIn("Mossan Store", email.subject)
        self.assertIn("このURLの有効期限は24時間です。", email.text)
        self.assertTrue(email.text.endswith("出欠ボード＋\n運営: Mossan Store"))

    def test_password_reset_uses_one_hour(self):
        email = build_password_reset_email(
            app_name="KYP",
            action_url="https://example.com/reset/token",
        )
        self.assertEqual(email.subject, "【KYP】パスワード再設定")
        self.assertIn("このURLの有効期限は1時間です。", email.text)
        self.assertNotIn("出欠ボード＋", email.text)

    def test_required_values(self):
        with self.assertRaises(ValueError):
            build_password_reset_email(app_name="", action_url="https://example.com")
        with self.assertRaises(ValueError):
            build_password_reset_email(app_name="KYP", action_url="")


if __name__ == "__main__":
    unittest.main()

