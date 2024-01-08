#!/usr/bin/python3
""" index.py - index file for api/v1/views folder """

from api.v1.views import app_views
from flask import jsonify
import models
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns a JSON status response """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Returns a JSON stats response """
    return jsonify({"amenities": models.storage.count(Amenity),
                    "cities": models.storage.count(City),
                    "places": models.storage.count(Place),
                    "reviews": models.storage.count(Review),
                    "states": models.storage.count(State),
                    "users": models.storage.count(User)}), 200
