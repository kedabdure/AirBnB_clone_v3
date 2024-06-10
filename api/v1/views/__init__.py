#!/usr/bin/python3
"""The blueprint for API"""
from flask import Blueprint

app_views = Blueprint(__name__, url_prefix='api/v1/')
