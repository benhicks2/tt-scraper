#!/usr/bin/env python3
"""
Program: ttserver

Description: A Flask REST API server to manage table tennis equipment data stored in MongoDB.

Usage: Run the included bash script to start the server.
"""
from flask import Flask, jsonify, request
from pymongo import MongoClient
import configparser

app = Flask(__name__)

# Setup MongoDB
config = configparser.ConfigParser()
config.read('config.ini')

client = MongoClient(config['database']['host'], config['database'].getint('port'))
db = client[config['database']['db_name']]


@app.route('/rubbers', methods=['GET'])
def get_rubbers():
    """
    Retrieve the matching rubbers from the database given a name.
    If no name is provided, return all rubbers.
    """
    return get_equipment('rubber', request)


@app.route('/blades', methods=['GET'])
def get_blades():
    """
    Retrieve the matching blades from the database given a name.
    If no name is provided, return all blades.
    """
    return get_equipment('blade', request)


@app.route('/equipment', methods=['GET'])
def get_equipment_options():
    """
    Return all available equipment types.
    """
    return jsonify(db.list_collection_names())


@app.route('/delete/<equipment_type>', methods=['DELETE'])
def delete_equipment(equipment_type):
    """
    Delete the specified equipment item.
    """
    collection_name = equipment_type + 's'
    if collection_name not in db.list_collection_names():
        return jsonify({'error': 'Invalid equipment type'}), 400

    data = request.get_json()
    if not data or 'name' not in data or 'site' not in data:
        return jsonify({'error': 'Invalid JSON body, name and site are required'}), 400

    name = data['name'].strip()
    site = data['site'].strip()

    collection = db[collection_name]

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


def get_equipment(equipment_type, request):
    """
    Return all matching equipment items given the name.
    If no name is provided, return all items of the given type.
    """
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


if __name__ == '__main__':
    app.run()
