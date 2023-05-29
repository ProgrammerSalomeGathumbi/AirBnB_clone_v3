#!/usr/bin/python3
"""
Create a new view for Amenity objects
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views, get, post, put, delete
from models import storage


@app_views.route("/amenities", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_crud(amenity_id=None):
    """Returns GET, POST, DELETE, PUT methods"""
    data = {
            'str': Amenity,
            'id': amenity_id,
            'p_id': None,
            'check': ['name'],
            'ignore': ['created_at', 'updated_at', 'id']}
    methods = {
                'GET': get,
                'POST': post,
                'DELETE': delete,
                'PUT': put}
    if request.method in methods:
        return methods[request.method](data)
