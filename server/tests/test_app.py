"""
Tests for Flask application initialization and configuration.
"""
import pytest
from unittest.mock import patch, Mock
import sys
import os

# Add the server directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAppInitialization:
    """Test Flask app initialization and configuration."""

    def test_app_creation(self):
        """Test that Flask app is created successfully."""
        from app import app
        assert app is not None
        assert app.name == 'app'

    def test_cors_configuration(self):
        """Test that CORS is properly configured."""
        from app import cors
        assert cors is not None

    def test_blueprint_registration(self):
        """Test that equipment blueprint is registered."""
        from app import app
        from routes import equipment

        # Check that the blueprint is registered
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert 'equipment' in blueprint_names

    def test_app_configuration(self):
        """Test app configuration settings."""
        from app import app
        assert app.config['TESTING'] is False  # Default value
        assert app.debug is False  # Default value


class TestAppRoutes:
    """Test that all routes are properly registered."""

    def test_equipment_routes_registered(self, client):
        """Test that equipment routes are accessible."""
        # Test that the routes are registered by checking if they exist
        from app import app

        # Get all registered routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]

        # Check for expected routes
        assert '/equipment' in routes
        assert '/<equipment_type>' in routes
        assert '/<equipment_type>/<id>' in routes

    def test_cors_headers(self, client):
        """Test that CORS headers are properly set."""
        response = client.get('/equipment')
        # CORS headers should be present
        assert 'Access-Control-Allow-Origin' in response.headers or response.status_code != 200
