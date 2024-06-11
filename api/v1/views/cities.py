#!/usr/bin/python3
"""
City module
Handles all default RESTFul API actions for State objects
"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State