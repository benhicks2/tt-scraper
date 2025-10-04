"""
Tests for Scrapy items functionality.
"""
import pytest
import scrapy
import sys
import os

# Add the server directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from equipment_scraper.items import EquipmentItem


class TestEquipmentItem:
    """Test EquipmentItem Scrapy item."""

    def test_equipment_item_creation(self):
        """Test EquipmentItem creation with all fields."""
        item = EquipmentItem()

        # Test that all expected fields exist
        assert '_id' in item.fields
        assert 'url' in item.fields
        assert 'name' in item.fields
        assert 'price' in item.fields

    def test_equipment_item_field_types(self):
        """Test that EquipmentItem fields are properly defined."""
        item = EquipmentItem()

        # All fields should be scrapy.Field instances
        for field_name, field in item.fields.items():
            assert isinstance(field, scrapy.Field)

    def test_equipment_item_set_fields(self):
        """Test setting fields on EquipmentItem."""
        item = EquipmentItem()

        item['_id'] = 'test_id_123'
        item['url'] = 'https://example.com/test'
        item['name'] = 'Test Equipment'
        item['price'] = '25.99'

        assert item['_id'] == 'test_id_123'
        assert item['url'] == 'https://example.com/test'
        assert item['name'] == 'Test Equipment'
        assert item['price'] == '25.99'

    def test_equipment_item_inheritance(self):
        """Test that EquipmentItem inherits from scrapy.Item."""
        item = EquipmentItem()
        assert isinstance(item, scrapy.Item)

    def test_equipment_item_field_access(self):
        """Test accessing fields on EquipmentItem."""
        item = EquipmentItem()

        # Test setting and getting fields
        item['name'] = 'Test Name'
        assert item['name'] == 'Test Name'

        # Test accessing non-existent field
        with pytest.raises(KeyError):
            _ = item['non_existent_field']

    def test_equipment_item_dict_conversion(self):
        """Test converting EquipmentItem to dictionary."""
        item = EquipmentItem()
        item['_id'] = 'test_id'
        item['url'] = 'https://example.com'
        item['name'] = 'Test Item'
        item['price'] = '19.99'

        item_dict = dict(item)

        assert item_dict['_id'] == 'test_id'
        assert item_dict['url'] == 'https://example.com'
        assert item_dict['name'] == 'Test Item'
        assert item_dict['price'] == '19.99'

    def test_equipment_item_empty_creation(self):
        """Test creating empty EquipmentItem."""
        item = EquipmentItem()

        # Empty item should have no values
        assert len(item) == 0

        # But should have all field definitions
        assert len(item.fields) == 4

    def test_equipment_item_partial_creation(self):
        """Test creating EquipmentItem with only some fields."""
        item = EquipmentItem()
        item['name'] = 'Partial Item'
        item['price'] = '15.99'

        assert item['name'] == 'Partial Item'
        assert item['price'] == '15.99'
        assert len(item) == 2

    def test_equipment_item_field_validation(self):
        """Test that EquipmentItem accepts various data types."""
        item = EquipmentItem()

        # Test string values
        item['name'] = 'String Name'
        assert item['name'] == 'String Name'

        # Test numeric values (as strings for price)
        item['price'] = '25.99'
        assert item['price'] == '25.99'

        # Test URL
        item['url'] = 'https://example.com/product/123'
        assert item['url'] == 'https://example.com/product/123'

        # Test ID
        item['_id'] = 'unique_id_123'
        assert item['_id'] == 'unique_id_123'

    def test_equipment_item_copy(self):
        """Test copying EquipmentItem."""
        original = EquipmentItem()
        original['name'] = 'Original Name'
        original['price'] = '20.00'

        # Create a copy by creating new item and copying fields
        copy = EquipmentItem()
        for key, value in original.items():
            copy[key] = value

        assert copy['name'] == original['name']
        assert copy['price'] == original['price']
        assert copy is not original

    def test_equipment_item_iteration(self):
        """Test iterating over EquipmentItem."""
        item = EquipmentItem()
        item['name'] = 'Test Name'
        item['price'] = '30.00'
        item['url'] = 'https://example.com'

        # Test iteration over keys
        keys = list(item.keys())
        assert 'name' in keys
        assert 'price' in keys
        assert 'url' in keys

        # Test iteration over values
        values = list(item.values())
        assert 'Test Name' in values
        assert '30.00' in values
        assert 'https://example.com' in values

        # Test iteration over items
        items = list(item.items())
        assert ('name', 'Test Name') in items
        assert ('price', '30.00') in items
