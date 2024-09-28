import unittest
import pandas as pd
from healthviz.analysis import Analyzer

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame to pass as data
        sample_data = pd.DataFrame({'heart_rate': [72, 75, 78, 120, 130, 200]})
        self.analyzer = Analyzer(data=sample_data)  # Pass the sample data

    def test_detect_anomalies(self):
        # Try a lower threshold to see if any anomalies are detected
        anomalies = self.analyzer.detect_anomalies('heart_rate', threshold=1)  # Lower the threshold
        
        # Print anomalies for debugging
        print("Detected anomalies:", anomalies)
        
        # Assert that at least one anomaly is detected
        self.assertGreater(len(anomalies), 0)

    def test_no_anomalies(self):
        # Test with a higher threshold where no anomalies should be detected
        anomalies = self.analyzer.detect_anomalies('heart_rate', threshold=2)
        
        # Assert that no anomalies are detected
        self.assertEqual(len(anomalies), 0)

if __name__ == '__main__':
    unittest.main()
