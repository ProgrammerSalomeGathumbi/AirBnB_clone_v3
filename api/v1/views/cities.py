#!/usr/bin/python3
"""
City objects that handles all default RESTFul API actions
"""
from flask import Flask
from flask import make_response, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id):
    """ list of all City objects of a State"""
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    c_dict = []
    for city in states.cities:
        c_dict.append(city.to_dict())
    return jsonify(c_dict)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city """
    state = storage.get(State, state_id)
    if not state:
        abort(400)
    cjson = request.get_json()
    if not cjson:
        abort(400, "Not a JSON")
    if "name" not in cjson:
        abort(400, "Missing name")
    cjson["state_id"] = state_id
    city = City(** cjson)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    cjson = request.get_json()
    if not cjson:
        abort(400, "Not a JSON")
    ignore = ["id", "created_at", "updated_at"]
    for key, value in cjson.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return make_responce(jsonify(city.to_dict()), 200)
