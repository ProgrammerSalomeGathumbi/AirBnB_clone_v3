#!/usr/bin/python3
"""
User objects that handles all default RESTFul API actions
"""
from flask import Flask
from flask import make_response, jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users", methods=['GET'],  strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    user = storage.all(User).values()
    s_dict = []
    for user in users:
        s_dict.append(user.to_dict())
    return jsonify(s_dict)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=['POST'],  strict_slashes=False)
def create_users():
    """Creates a User """
    rjson = request.get_json()
    if not rjson:
        abort(400, "Not a JSON")
    if "email" not in rjson:
        abort(400, "Missing email")
    if "password" not in rjson:
        abort(400, "Missing password")
    user = User(** rjson)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/user/<user_id>", methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    rjson = request.get_json()
    if not rjson:
        abort(400, "Not a JSON")
    ignore = ["id", "email",  "created_at", "updated_at"]
    for key, value in rjson.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_responce(jsonify(user.to_dict()), 200)
