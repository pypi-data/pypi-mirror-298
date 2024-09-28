import unittest
import pandas as pd
import numpy as np
from healthviz.data_handling import DataHandler

class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.handler = DataHandler()
        
    def test_normalize_data(self):
        # Create sample data
        data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        self.handler.data = data
        
        # Normalize the data
        self.handler.normalize_data(['A', 'B'])
        
        # Check that the mean of each column is close to 0
        for column in ['A', 'B']:
            np.testing.assert_almost_equal(self.handler.data[column].mean(), 0, decimal=5)

if __name__ == '__main__':
    unittest.main()
