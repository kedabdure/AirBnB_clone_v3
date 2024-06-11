#!/usr/bin/python3
"""
States file for api
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getAllStates():
    """Retrieves the list of all State objects"""
    retval = []
    all_states = storage.all(State)
    for item in all_states.values():
        retval.append(item.to_dict())
    return jsonify(retval)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def GET_state(state_id):
    """GET State object, else raise 404"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def DEL_state(state_id):
    """Delete a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def POST_state():
    """Adds state, raise 400 if not valid JSON"""
    post_content = request.get_json()

    if not request.is_json:
        abort(400, description="Not a JSON")

    name = post_content.get('name')
    if not name:
        abort(400, description="Missing name")

    # send in user input(key:value) to create new object
    new_state = State(**post_content)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def PUT_state(state_id):
    """Updates a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at"]

    content = request.get_json()

    if not request.is_json:
        abort(400, description="Not a JSON")

    for key, val in content.items():
        if key not in ignore_keys:
            setattr(state, key, val)

    state.save()
    return jsonify(state.to_dict())
