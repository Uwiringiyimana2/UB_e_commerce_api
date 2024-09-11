#!/usr/bin/env python3
""" Cart module
"""
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from models.base import Base, Base_model


class Cart(Base, Base_model):
    """ Cart model
    """
    __tablename__ = "carts"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    items = relationship("CartItem", backref="cart", cascade="all, delete-orphan")

    __table_args__ = {'extend_existing': True}

    @property
    def total_price(self):
        """ Calculate total price dynamically
        """
        from models.db import DB
        from models.product import Product
        db = DB()
        return sum(
          [db.get(Product, id=item.product_id).price * item.quantity for item in self.items]
        )


class CartItem(Base, Base_model):
    """ CartItem Model
    """
    __tablename__ = "cart_items"
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="unique_cart_product"),
        {'extend_existing': True}
    )
