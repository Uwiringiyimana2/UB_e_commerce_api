#!/usr/bin/env python3
""" cart endpoint module
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.db import DB
from models.product import Product
from models.cart import Cart, CartItem
from utils import token_required
from api.v1.config import Config


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