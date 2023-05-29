#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions
"""
from flask import Flask
from flask import make_response, jsonify, abort, request
from models import storage
from api.v1.views import app_views, get, delete, post, put


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
@app_views.route("/states/<states_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_curd(state_id=None):
    """Returns GET, POST, DELETE, PUT methods"""
    data = {
            'str': State,
            'id': state_id,
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
