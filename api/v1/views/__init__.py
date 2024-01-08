#!/usr/bin/python3
""" __init__ file for api/v1/views folder"""

from flask import Blueprint

# create a variable app_views which is an instance of Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

