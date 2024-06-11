#!/usr/bin/python3
"""State objects view for API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    """Retrieves object of state_id of State objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state)


@app_views.route('/states/<state_id', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods='POST', strict_slashes=False)
def post_states():
    """post states to the api"""
    if not request.json:
        abort(404, description='Not a JSON')
    if 'name' not in request.json:
        abort(404, description='Missing name')
    state = State(**request.json)
    storage.new(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods='PUT', strict_slashes=False)
def update_state(state_id):
    """update the state by state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(404, description='Not a JSON')
    ignore_key = ['id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_key:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
