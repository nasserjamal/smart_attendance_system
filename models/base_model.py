#!/usr/bin/python3
"""Contains BaseModel class"""

import json
import uuid
import models
from os import getenv
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz
Base = declarative_base()


class BaseModel:
    """Base class from which all other classes inherit"""
    def __init__(self, *args, **kwargs):
        """Initialization of the BaseModel class"""
        if kwargs:
            for key, value in kwargs.items():
                if key in ['start_time', 'end_time']:
                    setattr(self, key, datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S.%f'))
                elif key != "__class__":
                    setattr(self, key, value)

    def get_json(self, *args):
        data = {}
        for arg in args:
            if arg in ['end_time', 'start_time']:
                utc_datetime_obj = getattr(self, arg)
                utc_tz = pytz.timezone('UTC')
                gmt_plus_3_tz = pytz.timezone('Etc/GMT-3')
                utc_datetime_obj = utc_tz.localize(utc_datetime_obj)
                gmt_plus_3_datetime_obj = utc_datetime_obj.astimezone(gmt_plus_3_tz)
                data[arg] = gmt_plus_3_datetime_obj.strftime("%Y-%m-%d %H:%M")
            elif hasattr(self, arg):
                data[arg] = getattr(self, arg)
        return data

    def convert_to_EAT(self, time):
        utc_tz = pytz.timezone('UTC')
        gmt_plus_3_tz = pytz.timezone('Etc/GMT-3')
        time = utc_tz.localize(time)
        gmt_plus_3_datetime_obj = time.astimezone(gmt_plus_3_tz)
        return gmt_plus_3_datetime_obj

    def update_object(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key in ['start_time', 'end_time']:
                    setattr(self, key, datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S.%f'))
                elif key != "__class__" and key != "id":
                    setattr(self, key, value)

