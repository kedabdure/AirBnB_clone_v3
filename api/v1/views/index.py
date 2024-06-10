#!/usr/bin/python3
"""index module"""
from flask import jsonify
from api.v1.views import app_views

@app_views('/status')
def get_status():
    """return status"""
    return jsonify({"status": "OK"})