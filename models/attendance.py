#!/usr/bin/python3
"""Contains Attendance class"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, DateTime


class Attendance(BaseModel, Base):
    """Represents class Attendance"""
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    session_id = Column(Integer, ForeignKey('sessions.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    student = relationship('Students', back_populates='attendances')
    session = relationship("Sessions", back_populates="attendances")

    def __init__(self, *args, **kwargs):
        """Instantiation for class Attendance"""
        super().__init__(*args, **kwargs)
