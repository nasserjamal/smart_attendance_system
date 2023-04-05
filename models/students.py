#!/usr/bin/python3
"""Contains class Students"""

import models
from models.base_model import Base, BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class Students(BaseModel, Base):
    """Representation of the Students class"""
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))
    reg_no = Column(String(50))
    attendances = relationship('Attendance', back_populates='student')

    def __init__(self, *args, **kwargs):
        """Instantiation for Students class"""
        super().__init__(*args, **kwargs)
