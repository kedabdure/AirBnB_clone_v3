#!/usr/bin/python3
"""
Reviews file for API
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    post_content = request.get_json()

    user_id = post_content.get('user_id')
    if user_id is None:
        abort(400, description="Missing user_id")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    text = post_content.get('text')
    if text is None:
        abort(400, description="Missing text")

    new_review = Review(**post_content)
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]

    if not request.is_json:
        abort(400, description="Not a JSON")

    content = request.get_json()
    if content is None:
        abort(400, description="Not a JSON")

    for key, val in content.items():
        if key not in ignore_keys:
            setattr(review, key, val)

    review.save()
    return jsonify(review.to_dict())
