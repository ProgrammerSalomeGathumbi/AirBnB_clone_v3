#!/usr/bin/python3
"""
index file
"""
from flask import Flask
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def api_status():
    """returns JSON status """
    return jsonify({"status": "OK"})
