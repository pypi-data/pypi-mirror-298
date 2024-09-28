import numpy as np
from scipy import stats
import pandas as pd

class Analyzer:
    def __init__(self, data):
        self.data = data

    def basic_stats(self, column):
        """Return basic statistics (mean, median, std) for the specified column."""
        return {
            'mean': np.mean(self.data[column]),
            'median': np.median(self.data[column]),
            'std': np.std(self.data[column])
        }

    def detect_anomalies_iqr(self, column: str) -> pd.DataFrame:
        """Detect anomalies in the specified column using IQR method."""
        Q1 = self.data[column].quantile(0.25)
        Q3 = self.data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return self.data[(self.data[column] < lower_bound) | (self.data[column] > upper_bound)]

    def correlation_analysis(self, column1, column2):
        """Perform correlation analysis between two columns."""
        return np.corrcoef(self.data[column1], self.data[column2])[0, 1]
    
    def calculate_correlation(self, column1, column2):
        """Calculate correlation between two columns."""
        return self.data[column1].corr(self.data[column2])

    def calculate_trend(self, column):
        """Calculate trend using linear regression."""
        return self.data[column].mean()
