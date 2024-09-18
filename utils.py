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
from models.product import Product
from models.cart import Cart, CartItem
from models.order import Order, OrderItem, PaymentStatus
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
import smtplib
import os


db = DB()
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


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


def allowed_file(filename):
    """ validate image
    """
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def add_to_cart(user_id, product_id, quantity):
    """ Adding product(item) to Cart
    """
    cart = db.get(Cart, user_id=user_id)
    if not cart:
        cart = Cart(user_id=user_id)
        cart.save()

    cart_item = db.get(CartItem, cart_id=cart.id, product_id=product_id)
    if cart_item:
        soh = check_stock(cart_item.product_id)
        if (cart_item.quantity + quantity) > soh:
            raise ValueError(f"Only {soh} units are available")
        cart_item.quantity += quantity
        db.save()
        return cart_item
    else:
        soh = check_stock(product_id)
        if quantity > soh:
            raise ValueError(f"Only {soh} units are available") 
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
        )
        try:
            new_item.save()
            return new_item
        except IntegrityError:
           db.rollback()
           raise ValueError("Failed to add item")


def check_stock(product_id):
    """ return avalaible stock
    """
    product = db.get(Product, id=product_id)
    if not product:
        raise ValueError(f"Product with {product_id} not found!")
    return product.inventory


def update_cart_item(user_id, product_id, quantity):
    """ Updates the quantity of a product in the cart
    """
    cart = db.get(Cart, user_id=user_id)
    if not cart:
        raise NoResultFound()
    
    cart_item = db.get(CartItem, cart_id=cart.id, product_id=product_id)
    if not cart_item:
        raise NoResultFound()

    if quantity == 0:
        db.delete(cart_item)
        db.save()
        return "deleted"

    soh = check_stock(product_id)
    if quantity > soh:
        raise ValueError(f"Only {soh} units are available!")

    cart_item.quantity = quantity
    db.save()
    return cart_item


def create_order(user_id, cart):
    """create order after payment
    """
    new_order = Order(
        user_id=user_id,
        total_amount=cart.total_price,
        payment_status=PaymentStatus.PAID
    )
    db.add(new_order)
    db.save()

    for item in cart.items:
        product = db.get(Product, id=item.product_id)
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(order_item)

    db.save()


def clear_cart(user_id):
    """ clear cart after payment
    """
    cart = db.get(Cart, user_id=user_id)
    if not cart:
        return jsonify({"error": "Not found!"})
    if cart:
        db.delete(cart)
        db.save()
        return jsonify({}), 200
    return jsonify({"error": "No product found in cart"})


def send_confirmation_email(current_user, total_amount):
    """ send email confirming payment
    """
    email_subject = "Order Confirmation"
    email_body = f"Your order for ${total_amount / 100:.2f} has been confirmed."

    sender = "uwiringiyimanaericmax2000@gmail.com"
    recipient = current_user.email
    #app_password = os.getenv("APP_PASSWORD")
    app_password = "jbbhanfjzwjldsyz"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, app_password)
            message = f"Subject: {email_subject}\n\n{email_body}"
            server.sendmail(sender, recipient, message)
            print(f"Confirmation email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")


def decrease_product_quantity(user_id):
    """ decrease product quantity after making order
    """
    cart = db.get(Cart, user_id=user_id)
    if not cart or len(cart.items) == 0:
        return jsonify({"error": "No cart found!"})
    
    for item in cart.items:
        product = db.get(Product, id=item.product_id)
        product.inventory -= item.quantity
    db.save()


def index_range(page: int, page_size: int = 5):
    """return a tuple of size two containing a start index and an end index
    """
    return (page - 1) * page_size, page * page_size


def get_page(data, page: int = 1, page_size: int = 5):
    """ get pages
    """
    assert isinstance(page, int)
    assert isinstance(page_size, int)
    assert page > 0
    assert page_size > 0

    start_idx, end_idx = index_range(page, page_size)
    if start_idx >= len(data):
        return []
    
    return data[start_idx:end_idx]