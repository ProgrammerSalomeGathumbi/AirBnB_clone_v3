#!/usr/bin/python3
"""
Place objects that handles all default RESTFul API actions
"""
from flask import Flask
from flask import make_response, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """Retrieves a Place object of a city """
    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    c_dict = []
    for place in cities.places:
        c_dict.append(place.to_dict())
    return jsonify(c_dict)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(400)
    cjson = request.get_json()
    if not cjson:
        abort(400, "Not a JSON")
    if "user_id" not in cjson:
        abort(400, "Missing user_id")
    if "name" not in cjson:
        abort(400, "Missing name")
    cjson["city_id"] = city_id
    place = Place(** cjson)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    rjson = request.get_json()
    if not rjson:
        abort(400, "Not a JSON")
    ignore = ["id", "user_id", "city_id" "created_at", "updated_at"]
    for key, value in rjson.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_responce(jsonify(place.to_dict()), 200)
