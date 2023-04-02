#!/usr/bin/python3
"""Contains BaseModel class"""

import json
import models
from os import getenv
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class BaseModel:
    """Base class from which all other classes inherit"""
    def __init__(self, *args, **kwargs):
        """Initialization of the BaseModel class"""
        pass

    def get_json(self, *args):
        data = {}
        for arg in args:
            if hasattr(self, arg):
                data[arg] = getattr(self, arg)
        return data
