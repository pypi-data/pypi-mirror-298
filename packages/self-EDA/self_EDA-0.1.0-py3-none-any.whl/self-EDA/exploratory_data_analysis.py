import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
import missingno as msno

class ExploratoryDataAnalysis:
    def __init__(self, data):
        """Initialize with data which can be a pandas DataFrame or a path to a CSV file."""
        if isinstance(data, pd.DataFrame):
            self.df = data
        else:
            try:
                self.df = pd.read_csv(data)
            except Exception as e:
                raise ValueError("Invalid input: must be a pandas DataFrame or a path to a CSV file.") from e

    def missing_data_summary(self):
        """Plot missing data as a matrix and a heatmap."""
        msno.matrix(self.df)
        plt.show()

        msno.heatmap(self.df)
        plt.show()

        missing_data = self.df.isnull().sum()
        print(f"Missing data per column:\n{missing_data}")
        return missing_data

    def distribution_analysis(self):
        """Plot the distribution of all numerical columns."""
        self.df.hist(bins=20, figsize=(15, 10))
        plt.tight_layout()
        plt.show()

    def correlation_analysis(self):
        """Perform and plot the correlation matrix for numeric features."""
        corr_matrix = self.df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title("Correlation Matrix")
        plt.show()

    def detect_outliers(self, column, threshold=1.5):
        """Detect outliers in a given column using the IQR method."""
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        print(f"Detected {len(outliers)} outliers in column {column}")
        return outliers

    def feature_importance(self, target_column, task='classification', n_estimators=10):
        """
        Estimate feature importance using a Random Forest model.
        Reduced n_estimators for faster tests.
        """
        X = self.df.drop(columns=[target_column])
        y = self.df[target_column]

        if task == 'classification':
            model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        else:
            model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)

        importances = pd.Series(model.feature_importances_, index=X.columns)
        return importances

