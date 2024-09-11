#!/usr/bin/env python3
""" DB module
"""
from models.user import User
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from datetime import datetime


classes = {"User": User}


class DB:
    """ DB class
    """
    def __init__(self):
        """ Initializes properties
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

        if getenv('UB_ENV') == "test":
            Base.metadata.drop_all(self._engine)

    @property
    def _session(self):
        """ create database session
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add(self, obj):
        """ add obj to database
        """
        self._session.add(obj)

    def save(self):
        """ Commit to database
        """
        self._session.commit()

    def all(self, cls=None):
        """ retrieve all class objects in database
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss]:
                objs = self._session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + str(obj.id)
                    new_dict[key] = obj
        return new_dict

    def get(self, cls, **kwargs):
        """ Get one Object
        """
        if cls not in classes.values():
            return None

        for key in kwargs:
            if not hasattr(cls, key):
                return None
        res = self._session.query(cls).filter_by(**kwargs).first()
        if res is None:
            return None
        return res

    def delete(self, obj=None):
        """ delete from current database session obj if not None
        """
        if obj is not None:
            self._session.delete(obj)
