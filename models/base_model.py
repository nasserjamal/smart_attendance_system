#!/usr/bin/python3
"""Contains BaseModel class"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """Base class from which all other classes inherit"""
    def __init__(self, *args, **kwargs):
        """Initialization of the BaseModel class"""
        pass

    def save(self):
        """saves the new object into the database"""
        models.storage.new(self)
        models.storage.save()
