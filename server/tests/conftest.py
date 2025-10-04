"""
Test configuration and fixtures for TT Scraper server tests.
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from pymongo import MongoClient
from bson import ObjectId
import datetime

# Add the server directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from routes.equipment import dp, is_month_old, MONTH_LENGTH
from equipment_scraper.pipelines import MongoPipeline, SiteEntry


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_mongo_client():
    """Mock MongoDB client for testing."""
    with patch('routes.equipment.MongoClient') as mock_client:
        mock_db = Mock()
        mock_collection = Mock()

        # Mock database operations
        mock_collection.find_one.return_value = None
        mock_collection.find.return_value = []
        mock_collection.count_documents.return_value = 0
        mock_collection.delete_one.return_value = Mock(deleted_count=0)
        mock_collection.update_one.return_value = Mock(matched_count=0)
        mock_collection.insert_one.return_value = Mock(inserted_id=ObjectId())
        mock_collection.create_index.return_value = None
        mock_collection.list_collection_names.return_value = ['blades', 'rubbers']

        # Configure mock_db to support __getitem__ and other operations
        mock_db.__getitem__ = Mock(return_value=mock_collection)
        mock_db.list_collection_names.return_value = ['blades', 'rubbers']

        # Mock the client to return the mock_db
        mock_client_instance = Mock()
        mock_client_instance.__getitem__ = Mock(return_value=mock_db)
        mock_client.return_value = mock_client_instance

        yield mock_client, mock_db, mock_collection


@pytest.fixture
def sample_equipment_data():
    """Sample equipment data for testing."""
    return {
        '_id': 'test_id_123',
        'name': 'Test Rubber',
        'all_time_low_price': '25.99',
        'entries': [
            {
                '_id': 'entry_1',
                'url': 'https://example.com/rubber1',
                'price': '25.99',
                'last_updated': datetime.datetime.now()
            },
            {
                '_id': 'entry_2',
                'url': 'https://example.com/rubber2',
                'price': '29.99',
                'last_updated': datetime.datetime.now() - datetime.timedelta(days=35)
            }
        ]
    }


@pytest.fixture
def sample_blade_data():
    """Sample blade data for testing."""
    return {
        '_id': 'blade_id_123',
        'name': 'Test Blade',
        'all_time_low_price': '45.99',
        'entries': [
            {
                '_id': 'blade_entry_1',
                'url': 'https://example.com/blade1',
                'price': '45.99',
                'last_updated': datetime.datetime.now()
            }
        ]
    }


@pytest.fixture
def mock_crawler_process():
    """Mock CrawlerProcess for testing."""
    with patch('routes.equipment.CrawlerProcess') as mock_process:
        mock_instance = Mock()
        mock_instance.crawl.return_value = None
        mock_instance.start.return_value = None
        mock_instance.stop.return_value = None
        mock_process.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    with patch('routes.equipment.configparser.ConfigParser') as mock_config_parser:
        mock_config = Mock()
        mock_config.read.return_value = None
        mock_config.__getitem__.return_value = {
            'host': 'mongodb://localhost',
            'port': 27017,
            'db_name': 'test_db'
        }
        mock_config_parser.return_value = mock_config
        yield mock_config
