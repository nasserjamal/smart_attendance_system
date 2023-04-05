#!/usr/bin/python3
"""Contains class Cameras"""

import models
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class Cameras(BaseModel, Base):
    """Representation of the Students class"""
    __tablename__ = 'cameras'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))
    ip = Column(String(50))
    sessions = relationship("Sessions", back_populates="camera")

    def __init__(self, *args, **kwargs):
        """Instantiation for cameras class"""
        super().__init__(*args, **kwargs)
