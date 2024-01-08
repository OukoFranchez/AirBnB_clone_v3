#!/usr/bin/python3
"""This module creates a new view for State objects"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
This function retrieves a list of all State objects.

It defines a GET request to the endpoint /states.

Returns:
    A JSON response containing a list of all
    State objects and a status code of 200.
"""
    states = storage.all(State)
    state_list = []
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list), 200


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
This function retrieves a State object by its id.

Parameters:
- state_id (int): The id of the state to retrieve.

Returns:
- tuple: A tuple containing the JSON
representation of the state object and the
HTTP status code.

Raises:
- 404: If the state object with the given id
does not exist.
"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    This function deletes a State object by its id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
This function creates a new State.

Parameters:
- None

Returns:
- A JSON response containing the newly
created State object and a status code of 201.

Raises:
- 400 Bad Request if the request body is not
a valid JSON or if the 'name' field is
missing.

Example Usage:
create_state()
"""
    state_json = request.get_json()
    if state_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in state_json:
        abort(400, 'Missing name')
    state = State(**state_json)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
This function updates a State object.

Parameters:
- state_id (int): The ID of the state object
to be updated.

Returns:
- JSON response: A JSON response containing
the updated state object and a status code of
200.

Raises:
- 400 Bad Request: If the request body is not
a valid JSON.
- 404 Not Found: If the state object with the
given ID does not exist.

"""
    state_json = request.get_json()
    if state_json is None:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in state_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
