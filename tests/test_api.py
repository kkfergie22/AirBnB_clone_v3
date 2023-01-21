import unittest
from flask import Flask
from api.v1.views.index import app_views
from models import storage


class TestAPI(unittest.TestCase):
    """Test for API endpoints"""

    def setUp(self):
        """Sets up test methods"""
        app = Flask(__name__)
        app.register_blueprint(app_views)
        self.client = app.test_client()

    def test_status_route(self):
        """Tests the /status route"""
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_stats_route(self):
        """Tests the /stats route"""
        response = self.client.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
                         "amenities": 0, "cities": 0, "places": 0, "reviews":
                         0, "states": 0, "users": 0})

    def test_teardown(self):
        """Tests the teardown method"""
        storage.close()
        self.assertEqual(storage._FileStorage__objects)

    def test_invalid_route(self):
        """Tests invalid routes"""
        response = self.client.get('/api/v1/invalid_route')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_stats_route_with_data(self):
        """Tests the /stats route with data"""
        # Create some data
        user = User(email="test@example.com", password="test")
        storage.new(user)
        storage.save()
        response = self.client.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "amenities": 0, "cities": 0, "places": 0, "reviews": 0, "states":
            0, "users": 1})

    def test_teardown_with_data(self):
        """Tests the teardown method with data"""
        user = User(email="test@example.com", password="test")
        storage.new(user)
        storage.save()
        storage.close()
        self.assertFalse(storage._FileStorage__objects)
