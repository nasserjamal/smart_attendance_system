#!/usr/bin/python3
"""Contains Attendance class"""

import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, Time


class Attendance(BaseModel, Base):
    """Represents class Attendance"""
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    session_id = Column(Integer, ForeignKey('sessions.session_id'))
    start_time = Column(Time)
    end_time = Column(Time)

    def __init__(self, *args, **kwargs):
        """Instantiation for class Attendance"""
        super().__init__(*args, **kwargs)
