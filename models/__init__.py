#!/usr/bin/python3
"""Instantiation for models package"""

from models.engine.db import DBStorage

storage = DBStorage()
storage.reload()
