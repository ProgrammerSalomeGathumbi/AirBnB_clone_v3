#!/usr/bin/python3
"""
Create a new view for Amenity objects
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage


@app_views.route("/amenities", methods=['GET'],  strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    s_dict = []
    for amenity in amenities:
        s_dict.append(amenity.to_dict())
    return jsonify(s_dict)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object """
    Amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenities_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=['POST'],  strict_slashes=False)
def create_amenity():
    """Creates an Amenity """
    rjson = request.get_json()
    if not rjson:
        abort(400, "Not a JSON")
    if "name" not in rjson:
        abort(400, "Missing name")
    amenity = Amenity(** rjson)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_state(amenity_id):
    """Updates an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    rjson = request.get_json()
    if not rjson:
        abort(400, "Not a JSON")
    ignore = ["id", "created_at", "updated_at"]
    for key, value in rjson.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_responce(jsonify(amenity.to_dict()), 200)
