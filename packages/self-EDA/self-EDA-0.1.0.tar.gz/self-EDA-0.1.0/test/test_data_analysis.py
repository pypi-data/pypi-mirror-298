import unittest
import pandas as pd
from easyData.data_analysis import EasyData

class TestEasyData(unittest.TestCase):
    def setUp(self):
        """Set up a simple DataFrame for testing."""
        data = {
            "A": [1, 2, 2, 4, 5],
            "B": [10, None, 30, 40, 50],
            "C": [100, 200, 300, 400, 500]
        }
        self.df = pd.DataFrame(data)
        self.easy_data = EasyData(self.df)

    def test_get_summary(self):
        summary = self.easy_data.get_summary()
        self.assertTrue('A' in summary.columns)
        self.assertTrue('B' in summary.columns)

    def test_calculate_mean(self):
        mean_A = self.easy_data.calculate_mean('A')
        self.assertEqual(mean_A, 2.8)

    def test_calculate_std(self):
        std_B = self.easy_data.calculate_std('B')
        self.assertAlmostEqual(std_B, 18.257, places=3)

    def test_remove_duplicates(self):
        result = self.easy_data.remove_duplicates()
        self.assertEqual(result, "Removed 1 duplicate rows.")
        self.assertEqual(len(self.easy_data.df), 4)

    def test_remove_nulls(self):
        result = self.easy_data.remove_nulls()
        self.assertEqual(result, "Removed 1 rows with null values.")
        self.assertFalse(self.easy_data.df.isnull().values.any())

    def test_standardize_data(self):
        self.easy_data.standardize_data(columns=['A', 'C'])
        mean_A = round(self.easy_data.df['A'].mean(), 5)
        std_C = round(self.easy_data.df['C'].std(), 5)
        self.assertEqual(mean_A, 0.0)
        self.assertAlmostEqual(std_C, 1.0, places=1)

if __name__ == '__main__':
    unittest.main()
