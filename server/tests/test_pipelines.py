"""
Tests for MongoDB pipeline functionality.
"""
import pytest
import hashlib
import datetime
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the server directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from equipment_scraper.pipelines import MongoPipeline, SiteEntry, RUBBER_COLLECTION_NAME, BLADE_COLLECTION_NAME


class TestSiteEntry:
    """Test SiteEntry class functionality."""

    def test_site_entry_initialization(self):
        """Test SiteEntry initialization with default values."""
        url = "https://example.com/test"
        price = "25.99"
        entry = SiteEntry(url, price)

        assert entry.url == url
        assert entry.price == price
        assert isinstance(entry.timestamp, datetime.datetime)

    def test_site_entry_initialization_with_timestamp(self):
        """Test SiteEntry initialization with custom timestamp."""
        url = "https://example.com/test"
        price = "25.99"
        custom_timestamp = datetime.datetime(2023, 1, 1, 12, 0, 0)
        entry = SiteEntry(url, price, custom_timestamp)

        assert entry.url == url
        assert entry.price == price
        assert entry.timestamp == custom_timestamp

    def test_site_entry_asdict(self):
        """Test SiteEntry asdict method."""
        url = "https://example.com/test"
        price = "25.99"
        timestamp = datetime.datetime(2023, 1, 1, 12, 0, 0)
        entry = SiteEntry(url, price, timestamp)

        result = entry.asdict()

        expected = {
            'url': url,
            'price': price,
            'last_updated': timestamp
        }
        assert result == expected

    def test_site_entry_compute_id(self):
        """Test SiteEntry compute_id method."""
        url = "https://example.com/test"
        entry = SiteEntry(url, "25.99")

        computed_id = entry.compute_id(url)
        expected_id = hashlib.sha256(url.encode('utf-8')).hexdigest()

        assert computed_id == expected_id
        assert len(computed_id) == 64  # SHA256 hex length

    def test_site_entry_compute_id_consistency(self):
        """Test that compute_id is consistent for same URL."""
        url = "https://example.com/test"
        entry1 = SiteEntry(url, "25.99")
        entry2 = SiteEntry(url, "30.99")  # Different price, same URL

        id1 = entry1.compute_id(url)
        id2 = entry2.compute_id(url)

        assert id1 == id2

    def test_site_entry_compute_id_different_urls(self):
        """Test that compute_id is different for different URLs."""
        url1 = "https://example.com/test1"
        url2 = "https://example.com/test2"
        entry = SiteEntry(url1, "25.99")

        id1 = entry.compute_id(url1)
        id2 = entry.compute_id(url2)

        assert id1 != id2


class TestMongoPipeline:
    """Test MongoPipeline class functionality."""

    def test_mongo_pipeline_initialization(self):
        """Test MongoPipeline initialization."""
        mongo_uri = "mongodb://localhost:27017"
        mongo_db = "test_db"
        pipeline = MongoPipeline(mongo_uri, mongo_db)

        assert pipeline.mongo_uri == mongo_uri
        assert pipeline.mongo_db == mongo_db
        assert pipeline.COLLECTION_NAME is None

    def test_mongo_pipeline_from_crawler(self):
        """Test MongoPipeline from_crawler class method."""
        mock_crawler = Mock()
        mock_crawler.settings.get.side_effect = lambda key: {
            'MONGO_URI': 'mongodb://localhost:27017',
            'MONGO_DATABASE': 'test_db'
        }.get(key)

        pipeline = MongoPipeline.from_crawler(mock_crawler)

        assert pipeline.mongo_uri == 'mongodb://localhost:27017'
        assert pipeline.mongo_db == 'test_db'

    def test_mongo_pipeline_open_spider(self):
        """Test MongoPipeline open_spider method."""
        with patch('equipment_scraper.pipelines.pymongo.MongoClient') as mock_client:
            pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")
            mock_spider = Mock()

            pipeline.open_spider(mock_spider)

            mock_client.assert_called_once_with("mongodb://localhost:27017")
            assert pipeline.client is not None
            assert pipeline.db is not None

    def test_mongo_pipeline_close_spider(self):
        """Test MongoPipeline close_spider method."""
        pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")
        pipeline.client = Mock()
        mock_spider = Mock()

        pipeline.close_spider(mock_spider)

        pipeline.client.close.assert_called_once()

    def test_mongo_pipeline_compute_id(self):
        """Test MongoPipeline compute_id method."""
        pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")

        item = {'name': 'Test Rubber'}
        computed_id = pipeline.compute_id(item)

        expected_id = hashlib.sha256('test rubber'.encode('utf-8')).hexdigest()
        assert computed_id == expected_id

    def test_mongo_pipeline_compute_id_case_insensitive(self):
        """Test that compute_id is case insensitive."""
        pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")

        item1 = {'name': 'Test Rubber'}
        item2 = {'name': 'TEST RUBBER'}
        item3 = {'name': 'test rubber'}

        id1 = pipeline.compute_id(item1)
        id2 = pipeline.compute_id(item2)
        id3 = pipeline.compute_id(item3)

        assert id1 == id2 == id3

    def test_mongo_pipeline_compute_id_whitespace_handling(self):
        """Test that compute_id handles whitespace correctly."""
        pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")

        item1 = {'name': 'Test Rubber'}
        item2 = {'name': ' Test Rubber '}
        item3 = {'name': '  Test Rubber  '}

        id1 = pipeline.compute_id(item1)
        id2 = pipeline.compute_id(item2)
        id3 = pipeline.compute_id(item3)

        assert id1 == id2 == id3

    @patch('equipment_scraper.pipelines.ItemAdapter')
    def test_mongo_pipeline_process_item_rubber_spider(self, mock_adapter):
        """Test process_item with rubber spider."""
        with patch('equipment_scraper.pipelines.pymongo.MongoClient') as mock_client:
            pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")
            mock_db = Mock()
            mock_collection = Mock()
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            mock_client.return_value.__getitem__.return_value = mock_db
            pipeline.client = mock_client.return_value
            pipeline.db = mock_db

            mock_spider = Mock()
            mock_spider.name = 'rubber_megaspin'

            item = {'name': 'Test Rubber', 'url': 'https://example.com', 'price': '25.99'}
            mock_adapter.return_value.asdict.return_value = item

            # Mock database operations
            mock_collection.update_one.return_value = Mock(matched_count=0)
            mock_collection.insert_one.return_value = Mock(inserted_id='test_id')
            mock_collection.find_one.return_value = None

            result = pipeline.process_item(item, mock_spider)

            assert result == item
            assert pipeline.COLLECTION_NAME == RUBBER_COLLECTION_NAME
            mock_collection.insert_one.assert_called_once()

    @patch('equipment_scraper.pipelines.ItemAdapter')
    def test_mongo_pipeline_process_item_blade_spider(self, mock_adapter):
        """Test process_item with blade spider."""
        with patch('equipment_scraper.pipelines.pymongo.MongoClient') as mock_client:
            pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")
            mock_db = Mock()
            mock_collection = Mock()
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            mock_client.return_value.__getitem__.return_value = mock_db
            pipeline.client = mock_client.return_value
            pipeline.db = mock_db

            mock_spider = Mock()
            mock_spider.name = 'blade_megaspin'

            item = {'name': 'Test Blade', 'url': 'https://example.com', 'price': '45.99'}
            mock_adapter.return_value.asdict.return_value = item

            # Mock database operations
            mock_collection.update_one.return_value = Mock(matched_count=0)
            mock_collection.insert_one.return_value = Mock(inserted_id='test_id')
            mock_collection.find_one.return_value = None

            result = pipeline.process_item(item, mock_spider)

            assert result == item
            assert pipeline.COLLECTION_NAME == BLADE_COLLECTION_NAME

    @patch('equipment_scraper.pipelines.ItemAdapter')
    def test_mongo_pipeline_process_item_update_existing(self, mock_adapter):
        """Test process_item updating existing item."""
        with patch('equipment_scraper.pipelines.pymongo.MongoClient') as mock_client:
            pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")
            mock_db = Mock()
            mock_collection = Mock()
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            mock_client.return_value.__getitem__.return_value = mock_db
            pipeline.client = mock_client.return_value
            pipeline.db = mock_db

            mock_spider = Mock()
            mock_spider.name = 'rubber_megaspin'

            item = {'name': 'Test Rubber', 'url': 'https://example.com', 'price': '25.99'}
            mock_adapter.return_value.asdict.return_value = item

            # Mock successful update
            mock_collection.update_one.return_value = Mock(matched_count=1)
            # Mock find_one to return None to avoid the price comparison
            mock_collection.find_one.return_value = None

            result = pipeline.process_item(item, mock_spider)

            assert result == item
            mock_collection.update_one.assert_called_once()

    @patch('equipment_scraper.pipelines.ItemAdapter')
    def test_mongo_pipeline_process_item_update_lowest_price(self, mock_adapter):
        """Test process_item updating lowest price."""
        with patch('equipment_scraper.pipelines.pymongo.MongoClient') as mock_client:
            pipeline = MongoPipeline("mongodb://localhost:27017", "test_db")
            mock_db = Mock()
            mock_collection = Mock()
            mock_db.__getitem__ = Mock(return_value=mock_collection)
            mock_client.return_value.__getitem__.return_value = mock_db
            pipeline.client = mock_client.return_value
            pipeline.db = mock_db

            mock_spider = Mock()
            mock_spider.name = 'rubber_megaspin'

            item = {'name': 'Test Rubber', 'url': 'https://example.com', 'price': '20.99'}
            mock_adapter.return_value.asdict.return_value = item

            # Mock successful update and existing item with higher price
            mock_collection.update_one.return_value = Mock(matched_count=1)
            mock_db_item = {
                '_id': 'test_id',
                'name': 'Test Rubber',
                'all_time_low_price': '25.99',
                'entries': []
            }
            # Create a mock that behaves like a dictionary
            mock_db_item_mock = Mock()
            mock_db_item_mock.__getitem__ = Mock(side_effect=lambda key: mock_db_item[key])
            mock_db_item_mock.__contains__ = Mock(side_effect=lambda key: key in mock_db_item)
            mock_db_item_mock.__bool__ = Mock(return_value=True)  # For 'if db_item' check
            mock_collection.find_one.return_value = mock_db_item_mock

            result = pipeline.process_item(item, mock_spider)

            assert result == item
            # Should update the lowest price
            assert mock_collection.update_one.call_count >= 2  # At least update and price update
