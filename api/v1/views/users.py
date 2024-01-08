#!/usr/bin/python3
"""This module creates a new view for user objects"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
This function retrieves a list of all User objects.

It defines a GET request to the endpoint /users.

Returns:
    A JSON response containing a list of User objects in dictionary format.
    The HTTP status code 200 indicating a successful request.
"""
    users = storage.all(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list), 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
This function retrieves a User object by its id.

Parameters:
- user_id (str): The id of the user to retrieve.

Returns:
- dict: A dictionary representation of the user object.

Raises:
- 404: If the user with the specified id does not exist.
"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """This function deletes a User object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
This function creates a new User.

Parameters:
    None

Returns:
    A JSON response containing the newly
    created User object and a status code of
    201.

Raises:
    400 Bad Request: If the request body is
    not a valid JSON or if the 'email' or
    'password' fields are missing.

Example Usage:
    create_user()
"""
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    if 'email' not in user_json:
        abort(400, 'Missing email')
    if 'password' not in user_json:
        abort(400, 'Missing password')
    user = User(**user_json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """
This function updates a User object.

Parameters:
- user_id: The ID of the user to be updated.

Returns:
- A JSON response containing the updated user
object and a status code of 200.

Raises:
- 400 Bad Request: If the request body is not
a valid JSON.
- 404 Not Found: If the user with the
specified ID does not exist.
"""
    user_json = request.get_json()
    if user_json is None:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for key, value in user_json.items():
        # Ignoring keys: id, email, created_at and updated_at
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
