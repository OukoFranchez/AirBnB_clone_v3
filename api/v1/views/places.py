#!/usr/bin/python3
"""This module creates a new view for user objects"""

from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.place import Place
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
Retrieves the list of all Place objects for a given city.

Parameters:
- city_id (str): The ID of the city.

Returns:
- JSON response: A JSON response
containing the list of all Place objects
for the given city.

Raises:
- 404 error: If the city with the given ID does not exist in the database.
"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
Retrieves a Place object.

Parameters:
- place_id (str): The ID of the place to retrieve.

Returns:
- dict: A dictionary representation of the Place object.

Raises:
- 404: If the place with the given ID does not exist.
"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
Deletes a Place object

Parameters:
- place_id (str): The ID of the place to be deleted

Returns:
- dict: An empty dictionary

Raises:
- 404: If the place with the given ID does not exist
"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
Creates a Place.

Parameters:
- city_id (str): The ID of the city where the place is located.

Returns:
- dict: A JSON representation of the created place.
- int: The HTTP status code 201.

Raises:
- HTTPException: If the city is not found,
the request is not in JSON format, the
user_id is missing, or the name is missing.
"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
Updates a Place object

Parameters:
- place_id (str): The ID of the Place object to be updated

Returns:
- tuple: A tuple containing the JSON
representation of the updated Place object
and the HTTP status code 200

Raises:
- 404: If the Place object with the given ID does not exist
- 400: If the request data is not in JSON format

"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
Retrieves all Place objects depending on search request.

Parameters:
- None

Returns:
- JSON response containing the search
results, or an error message if the search
request is not valid.

Example Usage:
places_search()
"""
    search_request = request.get_json()
    if not search_request or not isinstance(search_request, dict):
        return jsonify({'error': "Not a JSON"}), 400

    if not search_request or not any(search_request.values()):
        places = []
        for place in storage.all(Place).values():
            places.append(place.to_dict())
        return jsonify(places), 200

    search_results = []
    states = search_request.get('states', [])
    cities = search_request.get('cities', [])
    amenities = search_request.get('amenities', [])
    all_places = []
    all_cities = []
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                if storage_t == 'db':
                    all_cities.extend(state.cities)
                else:
                    all_cities.extend(state.cities())

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city and city not in all_cities:
                all_cities.append(city)

    city_ids = [city.id for city in all_cities]
    for place in storage.all(Place).values():
        if place.city_id in city_ids:
            all_places.append(place)

    if amenities:
        for place in all_places:
            place_amenities = []    # store amenities in a place
            if storage_t == 'db':
                place_amenities.extend(place.amenities)
            else:
                place_amenities.extend(place.amenities())
            if all(amenity in place_amenities for amenity in amenities):
                search_results.append(place.to_dict())
    else:
        for place in all_places:
            search_results.append(place.to_dict())

    return jsonify(search_results), 200
