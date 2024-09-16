#!/usr/bin/env python3
""" cart endpoint module
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.db import DB
from models.product import Product
from models.cart import Cart, CartItem
from utils import token_required, add_to_cart, update_cart_item
from api.v1.config import Config
from sqlalchemy.orm.exc import NoResultFound


db = DB()


@app_views.route("/cart", methods=["GET"], strict_slashes=False)
@token_required
def view_cart(current_user):
    """ view the products currently in your cart
    GET api/v1/cart
    """
    cart = db.get(Cart, user_id=current_user.id)
    if not cart:
        return jsonify({"error": "No Cart found"}), 404

    items = []
    for item in cart.items:
        items.append(item.to_dict())
    return jsonify({
      "items": items,
      "totalPrice": cart.total_price,
    })


@app_views.route("/cart/add/<product_id>", methods=["POST"], strict_slashes=False)
@token_required
def add_cart_item(current_user, product_id):
    """ add cart item to your cart
    POST api/v1/cart/add/<product_id>
    """
    quantity = request.form.get("quantity", 1)
    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "Invalid quantity type!"})
    try:
        item = add_to_cart(
          user_id=current_user.id,
          product_id=product_id,
          quantity=quantity,
        )
        if item:
            return jsonify(item.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)})


@app_views.route("/cart/remove/<product_id>", methods=["DELETE"], strict_slashes=False)
@token_required
def remove_cart_item(current_user, product_id):
    """ remove cart item to your cart
    DELETE api/v1/cart/remove/<product_id>
    """
    cart = db.get(Cart, user_id=current_user.id)
    if not cart:
        return jsonify({"error": "Not found"}), 404

    cart_item = db.get(CartItem, cart_id=cart.id, product_id=product_id)
    if cart_item:
        db.delete(cart_item)
        db.save()
        return jsonify({}), 200
    return jsonify({"error": "No product found in cart"})


@app_views.route("/cart/update/<product_id>", methods=["PUT"], strict_slashes=False)
@token_required
def update_item_quantity(current_user, product_id):
    """ Updates the quantity of a product in the cart
    PUT api/v1/cart/update/<product_id>
    """
    quantity = request.form.get("quantity")
    if not quantity:
        return jsonify({"error": "Missing quantity!"})

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "Invalid quantity!"}), 400

    try:
        updated_item = update_cart_item(current_user.id, product_id, quantity)
        if updated_item == "deleted":
           return jsonify({"message": "Product removed from th cart"}), 200
        return jsonify(updated_item.to_dict())
    except NoResultFound:
        return jsonify({"error": "Not found!!!"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
