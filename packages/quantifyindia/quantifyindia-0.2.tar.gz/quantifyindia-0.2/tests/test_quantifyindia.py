# tests/test_quantifyindia.py

import unittest
from quantifyindia import get_realtime_data, get_historical_data

class TestQuantifyIndia(unittest.TestCase):

    def test_get_realtime_data(self):
        result = get_realtime_data('RELIANCE')
        self.assertIn('symbol', result)

    def test_get_historical_data(self):
        result = get_historical_data('RELIANCE', '2023-01-01', '2023-12-31')
        self.assertIsInstance(result, dict)

if __name__ == '__main__':
    unittest.main()
