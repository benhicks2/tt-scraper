from flask import jsonify, request, Blueprint
from flask_cors import cross_origin
from pymongo import MongoClient
from bson.objectid import ObjectId
import configparser
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

config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient(config['database']['host'], config['database'].getint('port'))
db = client[config['database']['db_name']]

db[BLADE_ENDPOINT].create_index([('name', 'text')])
db[RUBBER_ENDPOINT].create_index([('name', 'text')])

@dp.route('/equipment', methods=['GET'])
def get_equipment_options():
    """
    Return all available equipment types.
    """
    return jsonify(db.list_collection_names())


@dp.route('/<equipment_type>', methods=['GET'])
@cross_origin()
def get_equipment(equipment_type):
    """
    Return all matching equipment items given the name.
    If no name is provided, return all items of the given type.
    """
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (equipment_type not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400

    items = db[equipment_type]
    cursor = None

    # Validate the input has a 'name' key
    equipment_name = request.args.get('name', None)
    cursor = request.args.get('cursor', None)

    # Pagination parameters
    if equipment_name:
        search = {'$text': {'$search': equipment_name}}
    else:
        search = {}
    if cursor:
        search['_id'] = {'$gt': cursor}

    # Search for the equipment in the database
    result = list(items.find(search).sort("_id", 1).limit(RETRIEVE_LIMIT))

    if not result or len(result) == 0:
        return jsonify({'error': f'No {equipment_type} found'}), 404
    if len(result) == 1:
        for entry in result[0]['entries']:
            entry['is_old'] = is_month_old(entry['last_updated'])
    return jsonify({
        'items': result,
        'next': str(result[-1]['_id']) if len(result) == RETRIEVE_LIMIT else "null"
    })


@dp.route('/<equipment_type>', methods=['DELETE'])
def delete_equipment(equipment_type):
    """
    Delete the specified equipment item.
    """
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (equipment_type not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400

    data = request.get_json()
    if not data or 'name' not in data or 'site' not in data:
        return jsonify({'error': 'Invalid JSON body, name and site are required'}), 400

    name = data['name'].strip()
    site = data['site'].strip()

    collection = db[equipment_type]

    # Check if the equipment item exists, and there's only one match
    num_matches = collection.count_documents({'name': {'$regex': name, '$options': 'i'}, 'url': {'$regex': site, '$options': 'i'}})
    if num_matches == 0:
        return jsonify({'error': f'No matches found for the {equipment_type[:-1]} "{name}" at "{site}"'}), 404
    if num_matches > 1:
        return jsonify({'error': f'Multiple matches found for the {equipment_type[:-1]} "{name}" at "{site}"'}), 400

    # Delete the equipment item
    result = collection.delete_one({'name': {'$regex': name, '$options': 'i'}, 'url': {'$regex': site, '$options': 'i'}})
    if result.deleted_count > 0:
        return jsonify({'status': 'success'}), 200
    return jsonify({'error': f'Unable to delete the {equipment_type[:-1]} "{name}" at "{site}"'}), 404


@dp.route('/<equipment_type>', methods=['PUT'])
def update_equipment(equipment_type):
    """
    Update the specified equipment item.
    """
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (equipment_type not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400

    process = CrawlerProcess(get_project_settings())

    if equipment_type == BLADE_ENDPOINT:
        process.crawl(BladeSpiderMegaspin)
        # process.crawl(BladeSpiderTT11)
    elif equipment_type == RUBBER_ENDPOINT:
        process.crawl(RubberSpiderMegaspin)
        # process.crawl(RubberSpiderTT11)
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
