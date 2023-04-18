#!/usr/bin/python3
"""Contains class DBStorage"""

from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, joinedload


class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self, *args, **kwargs):
        """Instantiation for class DBStorage"""
        MYSQL_USER = "smart_attendance_dev"# getenv('MYSQL_USER')
        MYSQL_PWD = "12345"# getenv('MYSQL_PWD')
        MYSQL_HOST = "localhost"# getenv('MYSQL_HOST')
        MYSQL_DB = "smart_attendance"# getenv('MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MYSQL_USER,
                                             MYSQL_PWD,
                                             MYSQL_HOST,
                                             MYSQL_DB))

    def new(self, obj):
        """Adds the object to the current session"""
        self.__session.add(obj)
        self.save()

    def save(self):
        """Commits the changes of the current session to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, fieldname="", value="", **filters):
        """
        Fetches a single object based on class, fieldname and value
        Parameters:
            cls: Name of the table to access
            fieldname(str): Name of the Column to be used
            value: Value to be used as the filter condition
        Usage:
            student1 = models.storage.get(Students, 'student_id', 1)
            print(student.name) # or perform any other operation
        """
        print(f"Length is {len(filters)}")
        if len(filters) != 0:
            query = self.__session.query(cls)
            for fieldname, value in filters.items():
                query = query.filter(getattr(cls, fieldname) == value)
            objct = query.first()
            return objct

        objct = self.__session.query(cls).filter(
            getattr(cls, fieldname) == value).first()
        return objct
    
    def get_all_greater(self, cls, fieldname, value):
        """
        Fetches a single object based on class, fieldname and value
        Parameters:
            cls: Name of the table to access
            fieldname(str): Name of the Column to be used
            value: Value to be used as the filter condition
        Usage:
            student1 = models.storage.get(Students, 'student_id', 1)
            print(student.name) # or perform any other operation
        """
        objct = self.__session.query(cls).filter(
            getattr(cls, fieldname) > value).all()
        return objct

    def get_all(self, *cls):
        """Returns a list of objects based on class"""
        query = self.__session.query(*cls)
        for i in range(len(cls) - 1):
            query = query.join(cls[i+1])
        return query.all()
    
    def all(self, cls, fieldname):
        """Returns a list containing data i.e not the entire class based on class and fieldname"""
        objct_list = []
        objcts = self.__session.query(cls)
        for objct in objcts:
            objct_list.append(getattr(objct, fieldname))
        return objct_list
    

    def fetch_and_delete(self, cls, fieldname, value):
        """Combines the get and delete method to fetch and delete in one go"""
        objct = self.get(cls, fieldname, value)
        self.delete(objct)

    def drop_all_tables(self):
        """Delete all data from all tables in the database"""
        # Get all tables
        metadata = MetaData(self.__engine)
        metadata.reflect()

        # Begin a new transaction
        self.__session.begin()

        # Iterate through all tables and delete data
        for table in reversed(metadata.sorted_tables):
            self.__session.execute(table.delete())
        # Commit the transaction
        self.__session.commit()

