#!/usr/bin/python3
"""
Amenity file for API
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = [
        amenity.to_dict() for amenity in storage.all(Amenity).values()
    ]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an Amenity"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    post_content = request.get_json()
    name = post_content.get('name')
    if name is None:
        abort(400, description="Missing name")

    new_amenity = Amenity(**post_content)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    ignore_keys = ["id", "created_at", "updated_at"]

    if not request.is_json:
        abort(400, description="Not a JSON")

    content = request.get_json()
    if content is None:
        abort(400, description="Not a JSON")

    for key, val in content.items():
        if key not in ignore_keys:
            setattr(amenity, key, val)

    amenity.save()
    return jsonify(amenity.to_dict())
