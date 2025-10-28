# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import pymongo
from datetime import datetime
import logging
import os

RUBBER_COLLECTION_NAME = 'rubbers'
BLADE_COLLECTION_NAME = 'blades'

class MongoPipeline:
    COLLECTION_NAME = None

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=os.getenv('MONGODB_URI'),
            mongo_db=os.getenv('MONGODB_DB_NAME'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_id = self.compute_id(item)
        site_entry = SiteEntry(url = item['url'], price = item['price'])

        if RUBBER_COLLECTION_NAME[:-1] in spider.name:
            self.COLLECTION_NAME = RUBBER_COLLECTION_NAME
        else:
            self.COLLECTION_NAME = BLADE_COLLECTION_NAME

        logging.info('Process item: %s', item['name'])

        # Try to update an existing site entry within an existing equipment item
        result = self.db[self.COLLECTION_NAME].update_one(
            filter={'_id': item_id, 'entries._id': site_entry._id},
            update={'$set': {'entries.$.price': site_entry.price, 'entries.$.last_updated': site_entry.timestamp}}
        )
        logging.info('Update existing site entry result: %s', result.raw_result)

        # If no existing site entry was updated, try to add a new site entry to existing equipment item
        if result.matched_count == 0:
            logging.info('Attempting to add new site entry for existing item: %s with ID %s', item['name'], item_id)
            result = self.db[self.COLLECTION_NAME].update_one(
                filter={'_id': item_id},
                update={'$push': {'entries': site_entry.asdict()}}
            )
            logging.info('Add new site entry result: %s', result.raw_result)

        # If even adding to existing item failed, create a new equipment item
        if result.matched_count == 0:
            logging.info('Creating new equipment item: %s with ID %s', item['name'], item_id)
            self.db[self.COLLECTION_NAME].insert_one({
                '_id': item_id,
                'name': item['name'],
                'all_time_low_price': site_entry.price,
                'entries': [site_entry.asdict()]
            })
        else:
            # An existing item was updated, update the cheapest price if necessary
            db_item = self.db[self.COLLECTION_NAME].find_one({'_id': item_id})
            if db_item and self._is_price_lower(site_entry.price, db_item['all_time_low_price']):
                logging.info('Updating lowest price for item: %s with ID %s', item['name'], item_id)
                self.db[self.COLLECTION_NAME].update_one(
                    filter={'_id': item_id},
                    update={'$set': {'all_time_low_price': site_entry.price}}
                )
        return item

    def compute_id(self, item):
        """
        Compute a unique ID for the item based on its name.
        """
        name = item['name'].casefold().strip()
        return hashlib.sha256((name).encode('utf-8')).hexdigest()

    def _is_price_lower(self, new_price: str, current_low_price: str) -> bool:
        """
        Compare two price strings to determine if the new price is lower.
        Handles different currencies and formats, converting EUR to USD for comparison.
        """
        try:
            # Extract numeric values from price strings
            import re

            def extract_price_value(price_str: str) -> float:
                numeric_part = re.sub(r'[^\d.,]', '', str(price_str))
                if ',' in numeric_part and '.' in numeric_part:
                    numeric_part = numeric_part.replace(',', '')
                elif ',' in numeric_part:
                    if numeric_part.count(',') == 1:
                        numeric_part = numeric_part.replace(',', '.')
                    else:
                        numeric_part = numeric_part.replace(',', '')

                return float(numeric_part)

            def detect_currency(price_str: str) -> str:
                """Detect currency from price string."""
                price_str = str(price_str).upper()
                if '€' in price_str or 'EUR' in price_str:
                    return 'EUR'
                elif '$' in price_str or 'USD' in price_str:
                    return 'USD'
                else:
                    # Default to USD if no currency symbol found
                    return 'USD'

            def convert_to_usd(price_value: float, currency: str) -> float:
                """Convert price to USD for comparison."""
                if currency == 'EUR':
                    # Using approximate EUR to USD conversion rate
                    # TODO: Pull real-time exchange rate
                    return price_value * 1.08
                else:
                    return price_value

            new_value = extract_price_value(new_price)
            current_value = extract_price_value(current_low_price)

            # Detect currencies and convert to USD
            new_currency = detect_currency(new_price)
            current_currency = detect_currency(current_low_price)

            new_value_usd = convert_to_usd(new_value, new_currency)
            current_value_usd = convert_to_usd(current_value, current_currency)

            return new_value_usd < current_value_usd
        except (ValueError, TypeError):
            return False


class SiteEntry():
    """
    Represents an entry in the equipment item database.
    """
    def __init__(self, url, price, timestamp=datetime.now()):
        self._id = self.compute_id(url)
        self.url = url
        self.price = price
        self.timestamp = timestamp

    def asdict(self):
        return { '_id': self._id, 'url': self.url, 'price': self.price, 'last_updated': self.timestamp }

    def compute_id(self, url):
        """
        Compute a unique ID for the site entry based on the URL.
        """
        return hashlib.sha256(url.encode('utf-8')).hexdigest()
