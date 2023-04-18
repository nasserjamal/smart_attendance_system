#!/usr/bin/python3
"""Contains class Sessions"""

import models
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime


class Sessions(BaseModel, Base):
    """Representation of class Sessions"""
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    camera_id = Column(Integer, ForeignKey('cameras.id'))
    camera = relationship("Cameras", back_populates="sessions")
    attendances = relationship("Attendance", back_populates="session")

    def __init__(self, *args, **kwargs):
        """Instantiation for Sessions class"""
        super().__init__(*args, **kwargs)
