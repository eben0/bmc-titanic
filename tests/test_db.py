import sqlite3
import unittest

from lib.db import Db


class TestDb(unittest.TestCase):
    def test_instance(self):
        db = Db.instance()
        client = db.get_db()
        self.assertTrue(isinstance(client, sqlite3.Connection))

    def test_read(self):
        db = Db.instance()
        client = db.get_db()
        row = client.cursor().execute("SELECT COUNT(*) as cnt FROM titanic").fetchone()
        self.assertEqual(row["cnt"], 891)


if __name__ == "__main__":
    unittest.main()
