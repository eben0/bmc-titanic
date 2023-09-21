import unittest

from lib.config import Config


class TestConfig(unittest.TestCase):
    def test_config(self):
        config = Config()
        self.assertTrue(isinstance(config, Config))
        self.assertDictEqual(
            config.get("db"),
            {
                "csv": "../assets/titanic.csv",
                "file": "../data/titanic.db",
                "table": "titanic",
            },
        )


if __name__ == "__main__":
    unittest.main()
