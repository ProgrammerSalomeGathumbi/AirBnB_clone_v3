#!/usr/bin/python3
"""
index file for restful api project
"""
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def api_status():
    """returns status """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def api_stats():
    """retrieves the number of each objects by type"""
    stats_dict = {"amenities": storage.count(Amenity),
                  "cities": storage.count(City),
                  "place": storage.count(Place),
                  "reviews": storage.count(Review),
                  "states": storage.count(State),
                  "users": storage.count(User)}
    return jsonify(stats_dict)
