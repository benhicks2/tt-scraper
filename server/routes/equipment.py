from flask import jsonify, request, Blueprint
from pymongo import MongoClient
import configparser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from equipment_scraper.spiders.blade_megaspin import BladeSpiderMegaspin
from equipment_scraper.spiders.rubber_megaspin import RubberSpiderMegaspin
from equipment_scraper.spiders.blade_tt11 import BladeSpiderTT11
from equipment_scraper.spiders.rubber_tt11 import RubberSpiderTT11

VALID_EQUIPMENT_TYPES = ['blade', 'rubber']

dp = Blueprint('equipment', __name__)

config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient(config['database']['host'], config['database'].getint('port'))
db = client[config['database']['db_name']]

process = CrawlerProcess(get_project_settings())


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
    collection_name = equipment_type + 's'
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (collection_name not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400

    items = db[f'{equipment_type}s']

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
    result = items.find().sort('name')
    output = []
    for equipment in result:
        if equipment_name.casefold() in equipment['name'].casefold():
            output.append(equipment)
    if output:
        return jsonify(output)
    return jsonify({'error': f'No {equipment_type}s found'}), 404


@dp.route('/<equipment_type>', methods=['DELETE'])
def delete_equipment(equipment_type):
    """
    Delete the specified equipment item.
    """
    collection_name = equipment_type + 's'
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (collection_name not in db.list_collection_names()):
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
        return jsonify({'error': f'No matches found for the {equipment_type} "{name}" at "{site}"'}), 404
    if num_matches > 1:
        return jsonify({'error': f'Multiple matches found for the {equipment_type} "{name}" at "{site}"'}), 400

    # Delete the equipment item
    result = collection.delete_one({'name': {'$regex': name, '$options': 'i'}, 'url': {'$regex': site, '$options': 'i'}})
    if result.deleted_count > 0:
        return jsonify({'status': 'success'}), 200
    return jsonify({'error': f'Unable to delete the {equipment_type} "{name}" at "{site}"'}), 404


@dp.route('/<equipment_type>', methods=['PUT'])
def update_equipment(equipment_type):
    """
    Update the specified equipment item.
    """
    collection_name = equipment_type + 's'
    if (equipment_type not in VALID_EQUIPMENT_TYPES) or (collection_name not in db.list_collection_names()):
        return jsonify({'error': 'Invalid equipment type'}), 400
    
    if equipment_type == 'blade':
        process.crawl(BladeSpiderMegaspin)
        # process.crawl(BladeSpiderTT11)
    elif equipment_type == 'rubber':
        process.crawl(RubberSpiderMegaspin)
        # process.crawl(RubberSpiderTT11)
    process.start(stop_after_crawl=True)
    # TODO: Add a websocket so we can continuously update the status
    return jsonify({'status': 'success'}), 200
