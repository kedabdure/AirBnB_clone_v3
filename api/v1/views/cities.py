#!/usr/bin/python3
"""
Cities file for API
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    post_content = request.get_json()
    name = post_content.get('name')
    if name is None:
        abort(400, description="Missing name")

    new_city = City(**post_content)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    ignore_keys = ["id", "state_id", "created_at", "updated_at"]

    if not request.is_json:
        abort(400, description="Not a JSON")

    content = request.get_json()
    if content is None:
        abort(400, description="Not a JSON")

    for key, val in content.items():
        if key not in ignore_keys:
            setattr(city, key, val)

    city.save()
    return jsonify(city.to_dict())
