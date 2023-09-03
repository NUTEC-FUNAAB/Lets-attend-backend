#!/usr/bin/env python3
""" Storage Class manager """
from contextlib import contextmanager
from dotenv.main import load_dotenv
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from sqlalchemy.pool import QueuePool

from models.base import Base
from models.user import User
from models.event import Event


load_dotenv()


class Storage:
    """ database storage class """

    __engine = None

    def __init__(self, **kwargs):
        """ initializes storage class """

        uname = environ["DB_ATTEND_USER"]
        passwd = environ["DB_ATTEND_PASSWORD"]
        dbname = environ["DB_ATTEND_NAME"]
        dbhost = environ["DB_ATTEND_HOST"]
        if environ["DB_ATTEND_MODE"] == "test" or kwargs.get("test", False):
            dbname = environ["DB_ATTEND_TEST_NAME"]
        """ Remove echo when done testing """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                uname, passwd, dbhost, dbname),
            pool_pre_ping=True,
            poolclass=QueuePool,
            pool_size=10)
        self.session_factory = sessionmaker(bind=self.__engine,
                                            expire_on_commit=False)
        self.Session = scoped_session(self.session_factory)
        if environ["DB_ATTEND_MODE"] == "test" or kwargs.get("test", False):
            Base.metadata.drop_all(self.__engine, checkfirst=True)

    def reload(self):
        """ Reloads the session and create tables """

        Base.metadata.create_all(self.__engine)

    @contextmanager
    def session_scope(self):
        """
            Creates a session, and tearsDown after control
            is transferred back
        """

        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise Exception
        finally:
            session.close()

    def all(self, cls=None):
        """ gets all objects """

        objects = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            with self.session_scope() as session:
                query = session.query(cls)
                for obj in query:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objects[key] = obj
        else:
            for model in [User, Event]:
                with self.session_scope() as session:
                    query = session.query(model)
                    for obj in query:
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        objects[key] = obj

        return objects

    def get(self, cls, id):
        """ gets a particular object """

        if type(cls) is str:
            cls = eval(cls)

        with self.session_scope() as session:
            try:
                obj = session.query(cls).filter(cls.id == id).one()
            except Exception:
                obj = None

        return obj

    def count(self, cls=None):
        """ Returns the number of objects of a class """

        return len(self.all(cls))

    def new(self, obj):
        """ Adds an object to the current session """

        with self.session_scope() as session:
            session.add(obj)

    def save(self):
        """ commits the current session """

        with self.session_scope() as session:
            session.commit()

    def delete(self, obj):
        """ deletes an object from the current session """

        with self.session_scope() as session:
            session.delete(obj)

    def close(self):
        """ removes the current session """

        self.Session.remove()
