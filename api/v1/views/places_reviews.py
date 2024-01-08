#!/usr/bin/python3
"""This module creates new view for user objects"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
Retrieves the list of all Review objects.

Parameters:
- place_id (str): The ID of the place to retrieve reviews for.

Returns:
- tuple: A tuple containing the JSON
representation of the reviews and the HTTP
status code (200).

Raises:
- 404: If the place with the given ID does not exist.
"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
Retrieves the list of all Review objects.

Parameters:
- place_id (str): The ID of the place to retrieve reviews for.

Returns:
- tuple: A tuple containing the JSON
representation of the reviews and the HTTP
status code (200).

Raises:
- 404: If the place with the given ID does not exist.
"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
Deletes a Review object

Parameters:
- review_id (str): The ID of the review to delete.

Returns:
- tuple: A tuple containing an empty JSON
response and the HTTP status code (200).

Raises:
- 404: If the review with the given ID does not exist.
"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
Creates a Review

Parameters:
- place_id: The ID of the place for which the
review is being created

Returns:
- A JSON response containing the newly created review and a status code of 201

Raises:
- 404 error if the place with the given
place_id does not exist
- 400 error if the request is not in JSON
format, or if the user_id or text is missing in the request
- 404 error if the user with the given
user_id does not exist
"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    new_review = Review(**request.get_json())
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """
Updates a Review object

Parameters:
- review_id (str): The ID of the review to update.

Returns:
- tuple: A tuple containing the JSON
representation of the updated review and the HTTP status code (200).

Raises:
- 404: If the review with the given ID does
not exist.
- 400: If the request is not in JSON format.
"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
