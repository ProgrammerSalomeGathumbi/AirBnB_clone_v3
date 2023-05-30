#!/usr/bin/python3
"""
Review objects that handles all default RESTFul API actions
"""
from flask import Flask
from flask import make_response, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ list of all Review objects of a Place"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)
    c_dict = []
    for review in places.reviews:
        c_dict.append(review.to_dict())
    return jsonify(c_dict)


@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object """
    review = storage.get(Review, review_id)
    if not city:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/review/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a review """
    place = storage.get(Place, place_id)
    if not place:
        abort(400)
    cjson = request.get_json()
    if not cjson:
        abort(400, "Not a JSON")
    if "name" not in cjson:
        abort(400, "Missing name")
    if "text" not in cjson:
        abort(400, "Missing text")
    cjson["place_id"] = place_id
    review = Review(** cjson)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    cjson = request.get_json()
    if not cjson:
        abort(400, "Not a JSON")
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in cjson.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return make_responce(jsonify(review.to_dict()), 200)
