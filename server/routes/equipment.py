from flask import jsonify, request, Blueprint
from flask_cors import cross_origin
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import datetime

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from equipment_scraper.spiders.blade_megaspin import BladeSpiderMegaspin
from equipment_scraper.spiders.rubber_megaspin import RubberSpiderMegaspin
from equipment_scraper.spiders.blade_tt11 import BladeSpiderTT11
from equipment_scraper.spiders.rubber_tt11 import RubberSpiderTT11

BLADE_ENDPOINT = 'blades'
RUBBER_ENDPOINT = 'rubbers'
VALID_EQUIPMENT_TYPES = [BLADE_ENDPOINT, RUBBER_ENDPOINT]
MONTH_LENGTH = 30
RETRIEVE_LIMIT = 10

dp = Blueprint('equipment', __name__)

client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_DB_NAME')]

db[BLADE_ENDPOINT].create_index([('name', 'text')])
db[RUBBER_ENDPOINT].create_index([('name', 'text')])


@dp.route('/<equipment_type>/<id>', methods=['GET'])
@cross_origin()
def get_equipment_item(equipment_type, id):
    """
    Return a specific equipment item by ID.
    """
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (equipment_type not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400

    item = db[equipment_type].find_one({'_id': id})
    if not item:
        return jsonify({'error': f'No {equipment_type[:-1]} found with ID {id}'}), 404
    return jsonify(item)


@dp.route('/<equipment_type>', methods=['GET'])
@cross_origin()
def get_equipment(equipment_type):
    """
    Return all matching equipment items given the name, up to
    RETRIEVE_LIMIT items.
    """
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (equipment_type not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400

    items = db[equipment_type]

    # Validate the input has a 'name' key
    equipment_name = request.args.get('name', None)
    page_str = request.args.get('page', '1')
    page = 1
    try:
        page = int(page_str)
    except ValueError:
        return jsonify({'error': 'Invalid page number'}), 400

    # Search for the equipment items
    result = []
    if equipment_name:
        result = list(items.find({'$text': {'$search': equipment_name}},
                                 {'score': {'$meta': 'textScore'}})
                           .sort([('score', {'$meta': 'textScore'}), ('_id', 1)])
                           .skip((page - 1) * RETRIEVE_LIMIT)
                           .limit(RETRIEVE_LIMIT))
    else:
        result = list(items.find({})
                           .skip((page - 1) * RETRIEVE_LIMIT)
                           .limit(RETRIEVE_LIMIT))


    if not result or len(result) == 0:
        return jsonify({'error': f'No {equipment_type} found'}), 404
    if equipment_name and result[0]['name'].lower() == equipment_name.lower():
        result = [result[0]]
    if len(result) == 1:
        for entry in result[0]['entries']:
            entry['is_old'] = is_month_old(entry['last_updated'])
    return jsonify({
        'items': result,
        'next': str(result[-1]['_id']) if len(result) == RETRIEVE_LIMIT else "null"
    })


@dp.route('/<equipment_type>', methods=['PUT'])
@cross_origin()
def update_equipment(equipment_type):
    """
    Update the specified equipment item.
    """
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (equipment_type not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400

    process = CrawlerProcess(get_project_settings())

    if equipment_type == BLADE_ENDPOINT:
        process.crawl(BladeSpiderMegaspin)
        process.crawl(BladeSpiderTT11)
    elif equipment_type == RUBBER_ENDPOINT:
        process.crawl(RubberSpiderMegaspin)
        process.crawl(RubberSpiderTT11)
    process.start(stop_after_crawl=True)
    # TODO: Add a websocket so we can continuously update the status
    process.stop()
    return jsonify({'status': 'success'}), 200


def is_month_old(timestamp: datetime) -> bool:
    """
    Check if the given timestamp is older than one month.
    """
    last_month = datetime.datetime.now() - datetime.timedelta(days=MONTH_LENGTH)
    return timestamp < last_month
