#!/usr/bin/env python3
""" app configurations
"""


class Config:
    """ config properties
    """
    SECRET_KEY = "c8f53c07-aa40-4901-9401-6895a429e8b0"
    JSONIFY_PRETTYPRINT_REGULAR = True
    UPLOAD_FOLDER = "static/images"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
