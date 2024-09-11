#!/usr/bin/env python3
"""Product model"""
from sqlalchemy import Column, String, Numeric, Integer
from models.base import Base_model, Base
from sqlalchemy.orm import relationship


class Product(Base_model, Base):
    """ Product class
    """
    __tablename__ = "products"
    name = Column(String(120), nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    description = Column(String(500), nullable=False)
    inventory = Column(Integer, nullable=False)
    category = Column(String(120), default="")
    imageURL = Column(String(250), nullable=False)

    cart_items = relationship("CartItem", backref="product", cascade="all, delete")
