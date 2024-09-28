import unittest
import pandas as pd
from healthviz.visualization import Visualizer
import matplotlib.pyplot as plt  # Import plt here
from unittest.mock import patch

class TestVisualizer(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame to pass as data
        sample_data = pd.DataFrame({'heart_rate': [72, 75, 78, 120, 130, 200]})
        self.visualizer = Visualizer(data=sample_data)  # Pass the sample data
        
    @patch('matplotlib.pyplot.show')  # Mock the show function
    def test_plot_histogram(self, mock_show):
        self.visualizer.plot_histogram('heart_rate')
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.show')  # Mock the show function
    def test_plot_scatter(self, mock_show):
        self.visualizer.plot_scatter('heart_rate', 'heart_rate')  # Same column for simplicity
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()
