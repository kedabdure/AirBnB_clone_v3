#!/usr/bin/python3
"""
User file for API
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    post_content = request.get_json()

    email = post_content.get('email')
    if email is None:
        abort(400, description="Missing email")

    password = post_content.get('password')
    if password is None:
        abort(400, description="Missing password")

    new_user = User(**post_content)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    ignore_keys = ["id", "email", "created_at", "updated_at"]

    if not request.is_json:
        abort(400, description="Not a JSON")

    content = request.get_json()
    if content is None:
        abort(400, description="Not a JSON")

    for key, val in content.items():
        if key not in ignore_keys:
            setattr(user, key, val)

    user.save()
    return jsonify(user.to_dict())
