"""
Tests for equipment routes functionality.
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from bson import ObjectId
import datetime
import sys
import os

# Add the server directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGetEquipmentOptions:
    """Test GET /equipment endpoint."""

    def test_get_equipment_options_success(self, client, mock_mongo_client):
        """Test successful retrieval of equipment options."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_db.list_collection_names.return_value = ['blades', 'rubbers']

        response = client.get('/equipment')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'blades' in data
        assert 'rubbers' in data

    def test_get_equipment_options_empty(self, client, mock_mongo_client):
        """Test equipment options when no collections exist."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_db.list_collection_names.return_value = []

        response = client.get('/equipment')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []


class TestGetEquipmentItem:
    """Test GET /<equipment_type>/<id> endpoint."""

    def test_get_equipment_item_success(self, client, mock_mongo_client, sample_equipment_data):
        """Test successful retrieval of equipment item."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.find_one.return_value = sample_equipment_data

        response = client.get('/rubbers/test_id_123')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['_id'] == 'test_id_123'
        assert data['name'] == 'Test Rubber'

    def test_get_equipment_item_invalid_type(self, client, mock_mongo_client):
        """Test retrieval with invalid equipment type."""
        response = client.get('/invalid_type/test_id')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid equipment type' in data['error']

    def test_get_equipment_item_not_found(self, client, mock_mongo_client):
        """Test retrieval of non-existent equipment item."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.find_one.return_value = None

        response = client.get('/rubbers/nonexistent_id')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No rubber found' in data['error']

    def test_get_equipment_item_collection_not_exists(self, client, mock_mongo_client):
        """Test retrieval when collection doesn't exist."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_db.list_collection_names.return_value = ['blades']  # No rubbers collection

        response = client.get('/rubbers/test_id')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestGetEquipment:
    """Test GET /<equipment_type> endpoint."""

    def test_get_equipment_with_name_success(self, client, mock_mongo_client, sample_equipment_data):
        """Test successful retrieval of equipment with name search."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.find.return_value = [sample_equipment_data]

        response = client.get('/rubbers?name=Test Rubber')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'items' in data
        assert len(data['items']) == 1
        assert data['items'][0]['name'] == 'Test Rubber'

    def test_get_equipment_without_name_success(self, client, mock_mongo_client, sample_equipment_data):
        """Test successful retrieval of equipment without name search."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.find.return_value = [sample_equipment_data]

        response = client.get('/rubbers')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'items' in data
        assert len(data['items']) == 1

    def test_get_equipment_invalid_type(self, client, mock_mongo_client):
        """Test retrieval with invalid equipment type."""
        response = client.get('/invalid_type')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_get_equipment_invalid_page(self, client, mock_mongo_client):
        """Test retrieval with invalid page number."""
        response = client.get('/rubbers?page=invalid')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid page number' in data['error']

    def test_get_equipment_not_found(self, client, mock_mongo_client):
        """Test retrieval when no equipment found."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.find.return_value = []

        response = client.get('/rubbers')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No rubbers found' in data['error']

    def test_get_equipment_exact_match(self, client, mock_mongo_client, sample_equipment_data):
        """Test exact name match returns single item."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        sample_equipment_data['name'] = 'Test Rubber'
        mock_collection.find.return_value = [sample_equipment_data]

        response = client.get('/rubbers?name=Test Rubber')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['items']) == 1

    def test_get_equipment_pagination(self, client, mock_mongo_client):
        """Test pagination functionality."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        # Create 11 items to test pagination
        items = [{'name': f'Item {i}', '_id': f'id_{i}'} for i in range(11)]
        mock_collection.find.return_value = items

        response = client.get('/rubbers?page=1')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'next' in data
        assert data['next'] == 'id_9'  # Last item ID when limit is 10

    def test_get_equipment_old_entries_marked(self, client, mock_mongo_client):
        """Test that old entries are marked as is_old."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        old_timestamp = datetime.datetime.now() - datetime.timedelta(days=35)
        sample_data = {
            '_id': 'test_id',
            'name': 'Test Rubber',
            'entries': [{
                '_id': 'entry_1',
                'url': 'https://example.com',
                'price': '25.99',
                'last_updated': old_timestamp
            }]
        }
        mock_collection.find.return_value = [sample_data]

        response = client.get('/rubbers?name=Test Rubber')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['items'][0]['entries'][0]['is_old'] is True


class TestDeleteEquipment:
    """Test DELETE /<equipment_type> endpoint."""

    def test_delete_equipment_success(self, client, mock_mongo_client):
        """Test successful deletion of equipment."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.count_documents.return_value = 1
        mock_collection.delete_one.return_value = Mock(deleted_count=1)

        data = {'name': 'Test Rubber', 'site': 'example.com'}
        response = client.delete('/rubbers', json=data)

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

    def test_delete_equipment_invalid_type(self, client, mock_mongo_client):
        """Test deletion with invalid equipment type."""
        data = {'name': 'Test Rubber', 'site': 'example.com'}
        response = client.delete('/invalid_type', json=data)

        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result

    def test_delete_equipment_invalid_json(self, client, mock_mongo_client):
        """Test deletion with invalid JSON body."""
        response = client.delete('/rubbers', json={})

        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Invalid JSON body' in result['error']

    def test_delete_equipment_not_found(self, client, mock_mongo_client):
        """Test deletion of non-existent equipment."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.count_documents.return_value = 0

        data = {'name': 'Non-existent Rubber', 'site': 'example.com'}
        response = client.delete('/rubbers', json=data)

        assert response.status_code == 404
        result = json.loads(response.data)
        assert 'error' in result
        assert 'No matches found' in result['error']

    def test_delete_equipment_multiple_matches(self, client, mock_mongo_client):
        """Test deletion when multiple matches found."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.count_documents.return_value = 2

        data = {'name': 'Ambiguous Rubber', 'site': 'example.com'}
        response = client.delete('/rubbers', json=data)

        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Multiple matches found' in result['error']

    def test_delete_equipment_deletion_failed(self, client, mock_mongo_client):
        """Test when deletion operation fails."""
        mock_client, mock_db, mock_collection = mock_mongo_client
        mock_collection.count_documents.return_value = 1
        mock_collection.delete_one.return_value = Mock(deleted_count=0)

        data = {'name': 'Test Rubber', 'site': 'example.com'}
        response = client.delete('/rubbers', json=data)

        assert response.status_code == 404
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Unable to delete' in result['error']


class TestUpdateEquipment:
    """Test PUT /<equipment_type> endpoint."""

    def test_update_rubbers_success(self, client, mock_crawler_process):
        """Test successful update of rubbers."""
        response = client.put('/rubbers')

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

        # Verify crawler was called
        mock_crawler_process.crawl.assert_called()
        mock_crawler_process.start.assert_called_once_with(stop_after_crawl=True)
        mock_crawler_process.stop.assert_called_once()

    def test_update_blades_success(self, client, mock_crawler_process):
        """Test successful update of blades."""
        response = client.put('/blades')

        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['status'] == 'success'

    def test_update_invalid_type(self, client, mock_crawler_process):
        """Test update with invalid equipment type."""
        response = client.put('/invalid_type')

        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
        assert 'Invalid equipment type' in result['error']

    @patch('routes.equipment.BladeSpiderMegaspin')
    @patch('routes.equipment.BladeSpiderTT11')
    def test_update_blades_crawlers_called(self, mock_blade_tt11, mock_blade_megaspin, client, mock_crawler_process):
        """Test that blade crawlers are called for blade updates."""
        response = client.put('/blades')

        assert response.status_code == 200
        mock_crawler_process.crawl.assert_any_call(mock_blade_megaspin)
        mock_crawler_process.crawl.assert_any_call(mock_blade_tt11)

    @patch('routes.equipment.RubberSpiderMegaspin')
    @patch('routes.equipment.RubberSpiderTT11')
    def test_update_rubbers_crawlers_called(self, mock_rubber_tt11, mock_rubber_megaspin, client, mock_crawler_process):
        """Test that rubber crawlers are called for rubber updates."""
        response = client.put('/rubbers')

        assert response.status_code == 200
        mock_crawler_process.crawl.assert_any_call(mock_rubber_megaspin)
        mock_crawler_process.crawl.assert_any_call(mock_rubber_tt11)
