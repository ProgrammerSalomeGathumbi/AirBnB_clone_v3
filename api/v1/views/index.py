#!/usr/bin/python3
"""This python script is part of the
first part of restful api project."""
from flask import Flask
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def api_status():
    """returns JSON status """
    return jsonify({'status': 'OK'})
