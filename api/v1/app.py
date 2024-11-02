#!/usr/bin/env python3
""" flssk app server
"""
from flask import Flask
from flask_cors import CORS
from api.v1.views import app_views
from api.v1.views import Config

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
app.register_blueprint(app_views)
CORS(app, resource={r"/api/v1/*": {"origins": "*"}})


@app.after_request
def ensure_pretty_print(response):
    if not app.debug:
        response.direct_passthrough = False
    return response


@app.route('/')
def home():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
