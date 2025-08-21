# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib
import pymongo
from datetime import datetime
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging

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
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item_id = self.compute_id(item)
        item_dict = ItemAdapter(item).asdict()
        site_entry = SiteEntry(url = item['url'], price = item['price'])

        if RUBBER_COLLECTION_NAME[:-1] in spider.name:
            self.COLLECTION_NAME = RUBBER_COLLECTION_NAME
        else:
            self.COLLECTION_NAME = BLADE_COLLECTION_NAME

        site_entry._id = site_entry.compute_id(site_entry.url)

        logging.info('Process item: %s', item['name'])

        # Try to update the item in the database if it exists
        result = self.db[self.COLLECTION_NAME].update_one(
            filter={'_id': item_id, 'entries._id': site_entry._id},
            update={'$set': {'entries.$[elem].price': site_entry.price}},
            array_filters=[{'elem._id': site_entry._id}]
        )

        # If no items were matched, insert a new array entry
        if result.matched_count == 0:
            logging.info('Attempting to insert new entry for item: %s with ID %s', item['name'], item_id)
            result = self.db[self.COLLECTION_NAME].update_one(
                filter={'_id': item_id},
                update={'$push': {'entries': site_entry.asdict()}}
            )

        # If even the array insert failed, insert a new rubber item
        if result.matched_count == 0:
            logging.info('Inserting new item: %s with ID %s', item['name'], item_id)
            self.db[self.COLLECTION_NAME].insert_one({
                '_id': item_id,
                'name': item['name'],
                'all_time_low_price': site_entry.price,
                'entries': [site_entry.asdict()]
            })
        else:
            # An existing item was updated, update the cheapest price if necessary
            db_item = self.db[self.COLLECTION_NAME].find_one({'_id': item_id})
            if db_item and db_item['all_time_low_price'] > site_entry.price:
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


class SiteEntry():
    """
    Represents an entry in the equipment item database.
    """
    def __init__(self, url, price, timestamp=datetime.now()):
        self.url = url
        self.price = price
        self.timestamp = timestamp

    def asdict(self):
        return { 'url': self.url, 'price': self.price, 'last_updated': self.timestamp }

    def compute_id(self, url):
        """
        Compute a unique ID for the site entry based on the URL.
        """
        return hashlib.sha256(url.encode('utf-8')).hexdigest()
