#!/usr/bin/python3
"""Contains BaseModel class"""

import json
import uuid
import models
from os import getenv
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class BaseModel:
    """Base class from which all other classes inherit"""
    def __init__(self, *args, **kwargs):
        """Initialization of the BaseModel class"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    def get_json(self, *args):
        data = {}
        for arg in args:
            if hasattr(self, arg):
                data[arg] = getattr(self, arg)
        return data
    

    def update_object(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__" and key != "id":
                    setattr(self, key, value)

