#!/usr/bin/python3
"""Create new view for the link between Place objects and Amenity objects"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
from models import storage_t


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
Retrieves the list of all Amenity objects of a Place.

Parameters:
- place_id: The ID of the Place object.

Returns:
- A JSON response containing the list of
Amenity objects of the Place and a status
code of 200.

Raises:
- 404 error if the Place object with the given ID does not exist.
"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = []
    place_amenities = []
    if storage_t == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenities()
    for amenity in amenities:
        place_amenities.append(amenity.to_dict())
    return jsonify(place_amenities), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
Delete an Amenity object from a Place.

Parameters:
- place_id (str): The ID of the Place.
- amenity_id (str): The ID of the Amenity.

Returns:
- Response: A JSON response indicating the success of the deletion.

Raises:
- 404 Error: If the Place or Amenity does not exist.
"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity not in place.amenities():
            abort(404)
        place.amenities().remove(amenity)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
Link a Amenity object to a Place

Parameters:
- place_id (str): The ID of the Place object
- amenity_id (str): The ID of the Amenity object

Returns:
- JSON response: The Amenity object in JSON format

Raises:
- 404 error: If the Place or Amenity object is not found
"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    place_amenities = []
    if storage_t == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenities()

    if amenity in place_amenities:
        return jsonify(amenity.to_dict()), 200
    place_amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
