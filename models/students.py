#!/usr/bin/python3
"""Contains class Students"""

import models
from models.base_model import Base, BaseModel
import sqlalchemy
from sqlalchemy import Column, Integer, String


class Students(BaseModel, Base):
    """Representation of the Students class"""
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50))
    reg_no = Column(String(50))

    def __init__(self, *args, **kwargs):
        """Instantiation for Students class"""
        super().__init__(*args, **kwargs)
