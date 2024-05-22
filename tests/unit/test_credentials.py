from unittest import TestCase

from tc_neo4j_lib.credentials import load_neo4j_credentials


class TestCredentialLoad(TestCase):
    def test_check_keys(self):
        creds = load_neo4j_credentials()

        self.assertIn("db_name", creds.keys())
        self.assertIn("url", creds.keys())
        self.assertIn("auth", creds.keys())

    def test_check_values(self):
        creds = load_neo4j_credentials()

        self.assertIsNotNone(creds["db_name"], None)
        self.assertIsNotNone(creds["url"], None)
        self.assertIsNotNone(creds["auth"], None)
