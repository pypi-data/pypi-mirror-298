import pandas as pd
import numpy as np

class DataHandler:
    def __init__(self):
        self.data = None

    def load_csv(self, file_path):
        """Load data from a CSV file."""
        self.data = pd.read_csv(file_path)
        return self

    def load_json(self, file_path):
        """Load data from a JSON file."""
        self.data = pd.read_json(file_path)
        return self

    def clean_data(self):
        """Remove NaN values from the dataset."""
        self.data = self.data.dropna()
        return self

    def normalize_data(self, columns):
        """Normalize specified columns in the dataset."""
        self.data[columns] = (self.data[columns] - self.data[columns].mean()) / self.data[columns].std()
        return self

    def resample_time_series(self, time_column, frequency):
        """Resample time series data based on the specified frequency."""
        self.data[time_column] = pd.to_datetime(self.data[time_column])
        self.data = self.data.set_index(time_column).resample(frequency).mean().reset_index()
        return self
