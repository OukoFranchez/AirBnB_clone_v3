#!/usr/bin/python3
"""This module creates an amenity objects view"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from flask import jsonify, abort, request


# Retrieves the list of all Amenity objects: GET /api/v1/amenities
@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """This function retrieves list of all amenity objects of a State"""
    amenities = storage.all(Amenity)
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list), 200


# Retrieves a Amenity object. : GET /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
This function retrieves an Amenity object.

Parameters:
- amenity_id (str): The ID of the Amenity object to be retrieved.

Returns:
- Response: A JSON response containing the retrieved Amenity object.

Raises:
- 404 Error: If the Amenity object with the specified ID does not exist.
"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict()), 200


# Deletes a Amenity object: DELETE /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
This function deletes a Amenity object.

Parameters:
- amenity_id (str): The ID of the Amenity object to be deleted.

Returns:
- Response: A JSON response indicating the success of the deletion.

Raises:
- 404 Error: If the Amenity object with the specified ID does not exist.
"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


# Creates a Amenity: POST /api/v1/amenities
@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """This function creates a new Amenity object"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    # store json data from request in a variable
    data = request.get_json()
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


# Updates a Amenity object: PUT /api/v1/amenities/<amenity_id>
@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    # """This function updates a Amenity object"""
    """
This function updates an Amenity object.

Parameters:
- amenity_id (str): The ID of the Amenity object to be updated.

Returns:
- Response: A JSON response containing the updated Amenity object.

Raises:
- 404 Error: If the Amenity object with the specified ID does not exist.
- 400 Error: If the request data is not in JSON format.
"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
