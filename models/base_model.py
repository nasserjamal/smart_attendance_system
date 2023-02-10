#!/usr/bin/python3
"""Contains BaseModel class"""

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
