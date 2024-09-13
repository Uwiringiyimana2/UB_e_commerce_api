#!/usr/bin/env python3
"""Order model"""
from sqlalchemy import Column, Integer, ForeignKey, Numeric, Enum
from models.base import Base_model, Base
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship


class PaymentStatus(PyEnum):
    """ payment status model
    """
    PAID = "Paid"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class Order(Base, Base_model):
    """ Order model
    """
    __tablename__ = "orders"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Numeric(precision=10, scale=2), nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PAID)

    order_items = relationship("OrderItem", backref="order", cascade="all, delete-orphan")


class OrderItem(Base, Base_model):
    """ OrderItem model
    """
    __tablename__ = "order_items"
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
