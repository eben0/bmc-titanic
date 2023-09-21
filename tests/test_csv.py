import unittest
import pandas as pd


class TestCSV(unittest.TestCase):

    def test_read(self):
        path_to_csv = "../assets/titanic.csv"
        df = pd.read_csv(path_to_csv)
        self.assertEqual(df["Fare"].count(), 891)


if __name__ == "__main__":
    unittest.main()
