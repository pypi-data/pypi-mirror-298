import unittest
import pandas as pd
import numpy as np
from oilgas_analysis.well_logs import analyze_well_log, load_well_log_data

class TestWellLogs(unittest.TestCase):
    def setUp(self):
        # Create a sample dataset for testing
        self.sample_data = pd.DataFrame({
            'DEPTH': np.arange(1000, 1100, 10),
            'GR': np.random.uniform(50, 100, 10),
            'NPHI': np.random.uniform(0.1, 0.3, 10),
            'SW': np.random.uniform(0.2, 0.8, 10)
        })

    def test_analyze_well_log(self):
        result = analyze_well_log(self.sample_data)
        
        self.assertIn('average_porosity', result)
        self.assertIn('estimated_permeability', result)
        self.assertIn('dominant_lithology', result)
        self.assertIn('net_pay', result)
        
        self.assertGreater(result['average_porosity'], 0)
        self.assertGreater(result['estimated_permeability'], 0)
        self.assertIn(result['dominant_lithology'], ['sandstone', 'shale'])
        self.assertGreaterEqual(result['net_pay'], 0)

    def test_load_well_log_data(self):
        # This test requires a sample CSV or Excel file
        # For this example, we'll just test the error handling
        with self.assertRaises(ValueError):
            load_well_log_data('nonexistent_file.txt')

if __name__ == '__main__':
    unittest.main()