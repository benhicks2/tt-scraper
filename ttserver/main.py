from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Setup MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ttequipment_db']


@app.route('/rubbers', methods=['GET'])
def get_rubbers():
    return get_equipment('rubber', request)


@app.route('/blades', methods=['GET'])
def get_blades():
    return get_equipment('blade', request)


@app.route('/equipment', methods=['GET'])
def get_equipment_options():
    return jsonify(db.list_collection_names())


@app.route('/delete/<equipment_type>', methods=['DELETE'])
def delete_equipment(equipment_type):
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

    print(name)

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
