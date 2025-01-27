#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions
"""
from flask import Flask
from flask import make_response, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=['GET'],  strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    s_dict = []
    for state in states:
        s_dict.append(state.to_dict())
    return jsonify(s_dict)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'],  strict_slashes=False)
def create_state():
    """Creates a State """
    rjson = request.get_json()
    if not rjson:
        abort(400, "Not a JSON")
    if "name" not in rjson:
        abort(400, "Missing name")
    state = State(**rjson)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    rjson = request.get_json()
    if not rjson:
        abort(400, "Not a JSON")
    ignore = ["id", "created_at", "updated_at"]
    for key, value in rjson.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_responce(jsonify(state.to_dict()), 200)
