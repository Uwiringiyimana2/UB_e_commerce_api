#!/usr/bin/env python3
""" app configurations
"""

import os

class Config:
    """ config properties
    """
    SECRET_KEY = "c8f53c07-aa40-4901-9401-6895a429e8b0"
    JSONIFY_PRETTYPRINT_REGULAR = True
    UPLOAD_FOLDER = os.path.join('static', 'images')  # Save images to static/images
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    STRIPE_PUBLISHABLE_KEY = "pk_test_51PyFPuHI4UNrqRh5X2Y5TszAOKNv5wBbT8N4W3kHUsd5xR5q8YPLE5m8ib9MQnI4qgRKstnNvCLTRUo3Gpex5OpO00KZD2SLgE"
    STRIPE_SECRET_KEY = "sk_test_51PyFPuHI4UNrqRh5DPRc8i2DrCuOiKVn8bul4SLygdxPu05O62cZ3abTa7FOzE5oH1wqsble579pV2iJFpRfA6Ku00lH8cc8A5"