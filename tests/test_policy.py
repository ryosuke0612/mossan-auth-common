import unittest

from mossan_auth_common.policy import DEFAULT_AUTH_POLICY, normalize_email, safe_next_path


class PolicyTests(unittest.TestCase):
    def test_decided_expirations(self):
        self.assertEqual(DEFAULT_AUTH_POLICY.signup_confirmation_hours, 24)
        self.assertEqual(DEFAULT_AUTH_POLICY.password_reset_hours, 1)

    def test_normalize_email(self):
        self.assertEqual(normalize_email("  USER@Example.COM "), "user@example.com")
        self.assertEqual(normalize_email(None), "")

    def test_safe_next_path_accepts_local_path(self):
        self.assertEqual(safe_next_path("/dashboard?tab=1", "/"), "/dashboard?tab=1")

    def test_safe_next_path_rejects_external_or_protocol_relative_url(self):
        self.assertEqual(safe_next_path("https://evil.example", "/dashboard"), "/dashboard")
        self.assertEqual(safe_next_path("//evil.example/path", "/dashboard"), "/dashboard")
        self.assertEqual(safe_next_path("dashboard", "/dashboard"), "/dashboard")

    def test_safe_next_path_rejects_backslashes_and_encoded_redirects(self):
        unsafe_values = (
            "/\\evil.example",
            "/\\\\evil.example",
            "/%5cevil.example",
            "/%255cevil.example",
            "/%2f%2fevil.example",
        )
        for value in unsafe_values:
            with self.subTest(value=value):
                self.assertEqual(safe_next_path(value, "/dashboard"), "/dashboard")

    def test_safe_next_path_rejects_control_characters(self):
        for value in ("/\nevil.example", "/%0devil.example", "/%250aevil.example"):
            with self.subTest(value=value):
                self.assertEqual(safe_next_path(value, "/dashboard"), "/dashboard")


if __name__ == "__main__":
    unittest.main()
