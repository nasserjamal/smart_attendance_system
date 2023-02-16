#!/usr/bin/python3
"""Contains class Sessions"""

import models
from models.base_model import Base, BaseModel
import sqlalchemy
from sqlalchemy import Column, Integer, String, Time


class Sessions(BaseModel, Base):
    """Representation of class Sessions"""
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))
    start_time = Column(Time)
    end_time = Column(Time)
    classroom = Column(String(50))

    def __init__(self, *args, **kwargs):
        """Instantiation for Sessions class"""
        super().__init__(*args, **kwargs)
