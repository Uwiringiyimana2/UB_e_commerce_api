#!/usr/bin/env python3
""" product endpoint module
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.db import DB
from models.product import Product
from utils import token_required, allowed_file
from werkzeug.utils import secure_filename
from api.v1.config import Config
import os


db = DB()


@app_views.route('/products', methods=["GET"], strict_slashes=False)
def get_all_products():
    """ Retrieve all products
    GET api/v1/products
    """
    products = db.all(Product).values()
    products_list = []
    for product in products:
        products_list.append(product.to_dict())
    return jsonify(products_list)


@app_views.route('/products/<product_id>', methods=["GET"], strict_slashes=False)
def get_one_product(product_id):
    """ Retrieve specific product
    GET api/v1/products
    """
    product = db.get(Product, id=product_id)
    if not product:
        return jsonify({"error": "Not found"}), 404

    return jsonify(product.to_dict())

# Admin routes

@app_views.route('/admin/products', methods=["POST"], strict_slashes=False)
@token_required
def create_products(current_user):
    """ Create new product
    POST api/v1/admin/products
    """
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    name = request.form.get("name")
    if not name:
        return jsonify({"error": "Missing product's name"}), 400

    price = request.form.get("price")
    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "Invalid price format"}), 400
    description = request.form.get("description")
    if not description:
        return jsonify({"error": "Missing product's description"}), 400

    inventory = request.form.get("inventory")
    try:
        inventory = int(inventory)
    except ValueError:
        return jsonify({"error": "Invalid inventory format"}), 400

    category = request.form.get("category")
    if not category:
        return jsonify({"error": "Missing product's category"}), 400

    image = request.files.get("image")
    if not image:
        return jsonify({'error': 'No file part'}), 400

    if image.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        imageURL = os.path.join(Config.UPLOAD_FOLDER, filename)
        image.save(imageURL)
    else:
        return jsonify({"error": "Invalid file format"}), 400

    product = Product(
        name=name,
        price=price,
        description=description,
        inventory=inventory,
        category=category,
        imageURL=imageURL,
    )
    db.add(product)
    db.save()
    return jsonify(product.to_dict()), 201


@app_views.route('/admin/products/<id>', methods=["PUT"], strict_slashes=False)
@token_required
def update_products(current_user, id):
    """ Update existing product
    PUT api/v1/admin/products/<id>
    """
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    if not request.get_json():
        return jsonify({"error": "Not valid JSON"}), 400

    product = db.get(Product, id=id)
    if not product:
        return jsonify({"error": "Not found"})

    ignore = ["id", "created_at", "updated_at", "name"]
    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(product, key, value)
    db.save()
    return jsonify(product.to_dict()), 200


@app_views.route('/admin/products/<id>', methods=["DELETE"], strict_slashes=False)
@token_required
def delete_product(current_user, id):
    """ Update existing product
    PUT api/v1/admin/products/<id>
    """
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 401

    product = db.get(Product, id=id)
    if not product:
        return jsonify({"error": "Not found"})

    db.delete(product)
    db.save()
    return jsonify({}), 200
