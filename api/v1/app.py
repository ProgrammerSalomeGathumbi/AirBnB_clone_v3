#!/usr/bin/python3
"""This python script is the first part
of the Restful api project."""
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={"*": {"origins": "0.0.0.0"}})

@app.errorhandler(404)
def api_notfound(err):
    """ returns a JSON-formatted 404 status response"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def api_teardown(exc):
    """calls storage.close """
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
