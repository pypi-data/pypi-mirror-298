import unittest
import pandas as pd
from easyData.exploratory_data_analysis import ExploratoryDataAnalysis


class TestExploratoryDataAnalysis(unittest.TestCase):
    def setUp(self):
        """Set up a small DataFrame for testing."""
        data = {
            "A": [1, 2, 3, 4, 5],
            "B": [10, 20, 30, 40, 50],
            "C": [100, 200, 300, None, 500],
            "D": [1, 0, 1, 0, 1]  # Classification target
        }
        self.df = pd.DataFrame(data)
        self.eda = ExploratoryDataAnalysis(self.df)
        self.eda.visualize = False  # Disable visualizations during testing

    def test_missing_data_summary(self):
        """Test missing data summary functionality."""
        missing_data = self.eda.missing_data_summary()
        self.assertEqual(missing_data['C'], 1)  # There is 1 missing value in column 'C'

    def test_distribution_analysis(self):
        """Test distribution analysis without plotting."""
        # Since we disabled visualization, we just want to ensure that no error occurs
        try:
            self.eda.distribution_analysis()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Distribution analysis failed with error: {e}")

    def test_correlation_analysis(self):
        """Test correlation analysis without plotting."""
        try:
            self.eda.correlation_analysis()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Correlation analysis failed with error: {e}")

    def test_outlier_detection(self):
        """Test the outlier detection method."""
        outliers = self.eda.detect_outliers('A')
        # There should be no outliers in this small dataset
        self.assertEqual(len(outliers), 0)

    def test_feature_importance_classification(self):
        """Test feature importance for a classification task."""
        importances = self.eda.feature_importance(target_column='D', task='classification', n_estimators=5)
        # Ensure the feature importance for 'A', 'B', and 'C' is calculated
        self.assertIn('A', importances.index)
        self.assertIn('B', importances.index)
        self.assertIn('C', importances.index)

    def test_feature_importance_regression(self):
        """Test feature importance for a regression task."""
        importances = self.eda.feature_importance(target_column='B', task='regression', n_estimators=5)
        # Ensure the feature importance for 'A' and 'C' is calculated for regression
        self.assertIn('A', importances.index)
        self.assertIn('C', importances.index)


if __name__ == '__main__':
    unittest.main()
