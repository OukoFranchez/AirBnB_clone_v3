#!/usr/bin/python3
"""This module creates new view for city objects"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
This function retrieves a City object.

Parameters:
- city_id (str): The ID of the city to retrieve.

Returns:
- JSON response: A JSON response containing
the City object in dictionary format.

Raises:
- 404 error: If the city with the specified ID does not exist.
"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
This function deletes a City object.

Parameters:
- city_id (str): The ID of the city to be deleted.

Returns:
- tuple: A tuple containing an empty JSON response and a status code of 200.

Raises:
- 404 Error: If the city with the given ID does not exist.
"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
This function creates a new City object.

Parameters:
- state_id: The ID of the state to which the city belongs.

Returns:
- A JSON response containing the newly
created city object and a status code of 201.

Raises:
- 404 error if the state with the given state_id does not exist.
- 400 error if the request is not in JSON format or
if the 'name' field is missing in the request JSON.

"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    data['state_id'] = state_id
    new_city = City(**data)  #
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
This function updates a City object.

Parameters:
- city_id (str): The ID of the city to be updated.

Returns:
- JSON response: A JSON response containing
the updated city object and a status code of 200.

Raises:
- 404 error: If the city with the given ID does not exist.
- 400 error: If the request data is not in JSON format.

"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
