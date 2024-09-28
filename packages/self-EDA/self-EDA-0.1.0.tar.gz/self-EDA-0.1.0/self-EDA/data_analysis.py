import pandas as pd
from sklearn.preprocessing import StandardScaler

class EasyData:
    def __init__(self, data):
        """Initialize with data which can be a pandas DataFrame or file path to CSV."""
        if isinstance(data, pd.DataFrame):
            self.df = data
        else:
            try:
                self.df = pd.read_csv(data)
            except Exception as e:
                raise ValueError("Invalid input: must be a pandas DataFrame or a path to a CSV file.") from e

    def get_summary(self):
        """Return a summary of the DataFrame."""
        return self.df.describe()

    def get_columns(self):
        """Return the list of column names."""
        return self.df.columns.tolist()

    def calculate_mean(self, column):
        """Return the mean of a specified column."""
        if column in self.df.columns:
            return self.df[column].mean()
        else:
            raise ValueError(f"Column {column} not found in the DataFrame.")

    def calculate_std(self, column):
        """Return the standard deviation of a specified column."""
        if column in self.df.columns:
            return self.df[column].std()
        else:
            raise ValueError(f"Column {column} not found in the DataFrame.")

    def remove_duplicates(self):
        """Remove duplicate rows from the DataFrame."""
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        final_count = len(self.df)
        return f"Removed {initial_count - final_count} duplicate rows."

    def remove_nulls(self):
        """Remove rows with null values from the DataFrame."""
        initial_count = len(self.df)
        self.df = self.df.dropna()
        final_count = len(self.df)
        return f"Removed {initial_count - final_count} rows with null values."

    def standardize_data(self, columns=None):
        if columns is None:
            columns = self.df.select_dtypes(include='number').columns
        else:
            columns = [col for col in columns if col in self.df.columns]

        # Standardization process (mean = 0, std = 1)
        self.df[columns] = (self.df[columns] - self.df[columns].mean()) / self.df[columns].std()

        return f"Standardized columns: {columns}"

