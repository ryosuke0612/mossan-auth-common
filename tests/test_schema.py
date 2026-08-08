import unittest

from mossan_auth_common.schema import AUTH_SCHEMA_VERSION, auth_schema


class SchemaContractTests(unittest.TestCase):
    def test_schema_version(self):
        self.assertEqual(AUTH_SCHEMA_VERSION, 1)

    def test_required_tables(self):
        tables = {table.name: table for table in auth_schema()}
        self.assertEqual(
            set(tables),
            {"admins", "pending_admin_signups", "admin_password_reset_tokens"},
        )

    def test_token_tables_store_hash_and_lifecycle(self):
        tables = {table.name: table for table in auth_schema()}
        for name in ("pending_admin_signups", "admin_password_reset_tokens"):
            columns = {column.name for column in tables[name].columns}
            self.assertIn("token_hash", columns)
            self.assertNotIn("token", columns)
            self.assertIn("created_at", columns)
            self.assertIn("expires_at", columns)
            self.assertIn("used_at", columns)

    def test_app_specific_fields_are_not_in_admins(self):
        admins = next(table for table in auth_schema() if table.name == "admins")
        columns = {column.name for column in admins.columns}
        self.assertNotIn("billing_status", columns)
        self.assertNotIn("active_project_id", columns)
        self.assertNotIn("last_attendance_updated_at", columns)


if __name__ == "__main__":
    unittest.main()

