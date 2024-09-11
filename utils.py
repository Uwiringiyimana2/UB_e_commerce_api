#!/usr/bin/env python3
""" some helpfull functions
"""
from functools import wraps
from flask import jsonify, request
from api.v1.config import Config
import bcrypt
import jwt
from models.db import DB
from models.user import User


db = DB()


def hashpassword(passwd):
    """ hashing password
    """
    password = passwd.encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def token_required(f):
    """ verify token """
    @wraps(f)
    def decorated(*args, **kwargs):
        """decorator"""
        token = None
        if "x-access-token" in request.headers:
            token = request.headers.get("x-access-token")
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = db.get(User, email=data["email"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated
