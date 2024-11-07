import unittest
from unittest.mock import patch
import json
import os
from app import app, process_berry_data

class TestBerryStatsApp(unittest.TestCase):

    @patch('requests.get')  # Mocking requests.get globally
    def test_all_berry_stats_success(self, mock_get):
        # Set test env as True
        os.environ['TEST_ENV'] = 'True'
        os.environ['POKE_API_URL'] = 'True'
        # Mock the data of each berry
        with patch('requests.get'):
            with app.test_client() as client:
                response = client.get('/allBerryStats')
                self.assertEqual(response.status_code, 200)
                self.assertIn('berries_names', json.loads(response.data))
                self.assertIn('min_growth_time', json.loads(response.data))
                self.assertIn('max_growth_time', json.loads(response.data))
                self.assertIn('mean_growth_time', json.loads(response.data))

    @patch('requests.get')  # Mocking requests.get globally
    def test_all_berry_stats_missing_env_var(self, mock_get):
        """Test case when POKE_API_URL and TEST_ENV is not set in the environment."""
        # Clear any existing environment variables for testing
        os.environ.pop('POKE_API_URL', None)
        os.environ.pop('TEST_ENV', None)

        with app.test_client() as client:
            response = client.get('/allBerryStats')
            self.assertEqual(response.status_code, 500)
            self.assertIn('POKE_API_URL environment variable is not set', response.data.decode())

    @patch('requests.get')  # Mocking requests.get globally
    def test_process_berry_data(self, mock_get):
        # Example input data for berries
        berry_data = [
            {"name": "berry1", "growth_time": 10},
            {"name": "berry2", "growth_time": 5},
            {"name": "berry3", "growth_time": 7},
        ]

        # Call process_berry_data and check the output
        result = process_berry_data(berry_data)
        result_json = json.loads(result)

        self.assertEqual(result_json['berries_names'], ['berry1', 'berry2', 'berry3'])
        self.assertEqual(result_json['min_growth_time'], "The minimum growth time is 5 hours. It belongs to the berry2 berry.")
        self.assertEqual(result_json['max_growth_time'], "The maximum growth time is 10 hours. It belongs to the berry1 berry.")
        self.assertEqual(result_json['mean_growth_time'], "The mean growth time of all berries is 7.333333333333333 hours.")
        self.assertIn('variance_growth_time', result_json)
        self.assertIn('frequency_growth_time', result_json)

if __name__ == '__main__':
    unittest.main()
