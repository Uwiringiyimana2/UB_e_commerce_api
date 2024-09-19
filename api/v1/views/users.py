#!/usr/bin/env python3
""" users endpoint
"""
from models.db import DB
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response
from utils import hashpassword, token_required
from api.v1.config import Config
from datetime import datetime, timedelta
import bcrypt
import jwt


db = DB()


@app_views.route("/", methods=["GET"], strict_slashes=False)
def status():
    """ test status
    """
    return jsonify({"status": "OK"})


@app_views.route("/register", methods=["POST"], strict_slashes=False)
def register():
    """ POST api/v1/register
    """
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "Missing email"}), 401
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "Missing password"}), 401
    name = request.form.get("name")
    if name is None:
        return jsonify({"error": "Missing name"}), 401
    role = request.form.get("role", None)

    user = db.get(User, email=email)
    if user:
        return jsonify({"message": "Already registered!"}), 400

    password = hashpassword(password)
    user = User(email=email, name=name, password=password, role=role)
    db.add(user)
    db.save()
    msg = f"{email} registered successful"
    return jsonify({
        "message": msg,
        "User": user.to_dict()
    })


@app_views.route("/login", methods=["POST"], strict_slashes=False)
def login():
    """ POST api/v1/login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "Missing email!"}), 401
    if not password:
        return jsonify({"error": "Missing password"}), 401

    user = db.get(User, email=email)
    if not user:
        return jsonify({"error": "user not found!"}), 404
    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        token = jwt.encode({
          "email": user.email,
          "name": user.name,
          "exp": datetime.utcnow() + timedelta(minutes=30),
        }, Config.SECRET_KEY)
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials!"})


@app_views.route('/users', methods=["GET"], strict_slashes=False)
@token_required
def get_all_users(current_user):
    """GET api/v1/users
    """
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    all_users = db.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
@token_required
def get_one_user(current_user, user_id):
    """GET api/v1/users/<user_id>
    """
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"})

    user = db.get(User, id=user_id)
    if not user:
        return jsonify({"error": "Not found"})
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
@token_required
def update_user(current_user, user_id):
    """PUT api/v1/users/<user_id>
    """
    user = db.get(User, id=user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404

    if user.id != current_user.id and current_user.role != "admin":
        return jsonify({"error": "Unauthorized to update this user!"}), 401

    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    db.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=["DELETE"], strict_slashes=False)
@token_required
def delete_user(current_user, user_id):
    """ DELETE api/v1/users/<user_id>
    """
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    user = db.get(User, id=user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404

    db.delete(user)
    db.save()
    return jsonify({}), 200
