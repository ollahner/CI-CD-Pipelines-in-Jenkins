import os
import unittest
import requests
from urllib.parse import urljoin

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up test case with API configuration."""
        self.base_url = os.environ.get("API_BASE_URL", "http://localhost:5556")
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def get_url(self, endpoint):
        """Helper method to build full URL for endpoints."""
        return urljoin(self.base_url, endpoint)

    def test_hello_endpoint_success(self):
        """Test the /api/hello endpoint returns correct data."""
        response = requests.get(
            self.get_url('/api/hello'),
            headers=self.headers,
            timeout=5
        )

        # Test status code
        self.assertEqual(response.status_code, 200)

        # Test content type
        self.assertIn('application/json', response.headers['Content-Type'])

        # Test response data
        data = response.json()
        self.assertEqual(data['message'], 'Hello wimmer')
        self.assertEqual(data['status'], 'success')

    def test_api_response_time(self):
        """Test that API responds within acceptable time limit."""
        response = requests.get(
            self.get_url('/api/hello'),
            headers=self.headers,
            timeout=5
        )
        self.assertLess(response.elapsed.total_seconds(), 1.0)  # Response should be under 1 second

if __name__ == '__main__':
    unittest.main()
