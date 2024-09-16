#!/usr/bin/env python3
""" cart endpoint module
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.db import DB
from models.product import Product
from models.cart import Cart, CartItem
from models.order import Order, OrderItem, PaymentStatus
from utils import (
    token_required,
    create_order,
    clear_cart,
    send_confirmation_email,
    decrease_product_quantity
)
from api.v1.config import Config
from sqlalchemy.orm.exc import NoResultFound
import stripe


stripe.api_key = Config.STRIPE_SECRET_KEY
db = DB()


@app_views.route("/checkout", methods=["POST"], strict_slashes=False)
@token_required
def checkout(current_user):
    """ handle payment gateways
    POST api/v1/checkout
    """
    payment_method_id = request.form.get("paymentMethodId")
    if not payment_method_id:
        return jsonify({"error": "Missing payment Id"}), 400

    cart = db.get(Cart, user_id=current_user.id)
    if not cart or len(cart.items) == 0:
        return jsonify({"error": "Cart is empty"}), 400

    total_amount = cart.total_price * 100
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(cart.total_price) * 100,
            currency='usd',
            payment_method=payment_method_id,
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects": "never"
            },
            confirm=True
        )

        if payment_intent.status == "succeeded":
            create_order(current_user.id, cart)
            decrease_product_quantity(current_user.id)
            clear_cart(current_user.id)
            send_confirmation_email(current_user, total_amount)

        return jsonify({
            "status": payment_intent.status,
            "payment_intent": payment_intent.id
        })
    except stripe.error.CardError as e:
        return jsonify({"error": str(e)}), 400
    except stripe.error.APIConnectionError as e:
        return jsonify({"error": str({e})}), 503


@app_views.route("/orders", methods=["GET"], strict_slashes=False)
@token_required
def get_orders(current_user):
    """ Get history of user's orders
    GET api/v1/orders
    """
    orders = current_user.orders
    if not orders:
        return jsonify({"error": "No orders found!"}), 404

    order_history = []
    for order in orders:
        order_data = {
            "order_id": order.id,
            "user_id": order.user_id,
            "total_amount": order.total_amount,
            "payment_status": order.payment_status.value,
            "timestamp": order.created_at,
            "cart_items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                } for item in order.order_items
            ]
        }
        order_history.append(order_data)

    return jsonify(order_history), 200
