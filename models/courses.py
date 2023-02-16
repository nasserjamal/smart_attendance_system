#!/usr/bin/python3
"""Contains class Courses"""

import models
from models.base_model import Base, BaseModel
import sqlalchemy
from sqlalchemy import Column, Integer, String, Time


class Courses(BaseModel, Base):
    """Representation of class Courses"""
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, nullable=False)
    department = Column(String(50))
    course = Column(String(50))
    course_title = Column(String(50))
    course_code = Column(String(50))
    year_of_study = Column(Integer)
    lecturer_name = Column(String(50))

    def __init__(self, *args, **kwargs):
        """Initialization of class Courses"""
        super().__init__(*args, **kwargs)
