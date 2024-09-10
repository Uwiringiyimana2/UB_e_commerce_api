#!/usr/bin/env python3
"""User model"""
from sqlalchemy import Column, String
from models.base import Base_model, Base


class User(Base_model, Base):
    """User model"""
    __tablename__ = "users"
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    role = Column(String(60), default='user')
