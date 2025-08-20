from flask import jsonify, request, Blueprint
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
def get_equipment(equipment_type):
    """
    Return all matching equipment items given the name.
    If no name is provided, return all items of the given type.
    """
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (equipment_type not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400

    items = db[equipment_type]

    # Pagination parameters
    cursor = request.args.get('cursor')
    id_val = {}
    if cursor:
        try:
            id_val = {'$gt': ObjectId(cursor)}
        except Exception:
            return jsonify({'error': 'Invalid cursor'}), 400

    # The user didn't provide an equipment name, so return all distinct names
    if not request.data:
        result = items.distinct('name')
        return jsonify(result)

    # The user provided an equipment name, so search for it
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON'}), 400

    # Validate the input has a 'name' key
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': f'{equipment_type} name is required'}), 400
    equipment_name = data['name'].strip()

    # Search for the equipment in the database
    result = items.find({'$text': {'$search': equipment_name}, '_id': id_val}).limit(RETRIEVE_LIMIT).sort('name')
    for equipment in result:
        for entry in equipment['entries']:
            entry['is_old'] = is_month_old(entry['last_updated'])
    if result.count() > 0:
        return result
    return jsonify({'error': f'No {equipment_type} found'}), 404


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
