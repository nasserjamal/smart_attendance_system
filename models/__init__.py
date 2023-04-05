#!/usr/bin/python3
"""Instantiation for models package"""

from models.attendance import Attendance
from models.cameras import Cameras
from models.sessions import Sessions
from .students import Students
from .engine.db import DBStorage

storage = DBStorage()
storage.reload()
Students()
Cameras()
Sessions()
Attendance()
