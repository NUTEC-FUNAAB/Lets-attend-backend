#!/usr/bin/env python3
""" Module for testing the storage engine """

import inspect
import json
import unittest
import pep8 as pycodestyle

from contextlib import contextmanager
from dotenv.main import load_dotenv
from os import getenv, environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from models.base import BaseModel
from models.engine.storage import Storage
from models.event import Event
from models.user import User


load_dotenv()
classes = {"Event": Event, "User": User}


class TestStorage(unittest.TestCase):
    """ Test cases for storage engine """

    def test_pep8(self):
        """ Test that pep8 requirements are met """

        for path in ['models/engine/storage.py',
                     'tests/test_models/test_engine/test_storage.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_all(self):
        """ Tests that the all method of the storage engine returns a dict """
        storage = Storage(test=True)
        storage.reload()
        u = User(
            first_name="John",
            last_name="Doe",
            email="johnDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000000")
        e = Event(
            name="Birthday",
            description="My birthday",
            event_type="public",
            start_time="2021-02-17T22:46:38.883037",
            end_time="2021-02-17T22:56:38.883037",
            location="San Francisco",
            host=u.id,
            price=0.00
            )
        storage.new(u)
        storage.new(e)
        self.assertIsInstance(storage.all(), dict)

    def test_new(self):
        """ Tests that the new method of the storage engine works """
        storage = Storage(test=True)
        storage.reload()
        u = User(
            first_name="John",
            last_name="Doe",
            email="johnDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000000")
        storage.new(u)
        self.assertIn("User.{}".format(u.id), storage.all())

    def test_get(self):
        """ Tests that the get method of the storage engine works """
        storage = Storage(test=True)
        storage.reload()
        u = User(
            first_name="John",
            last_name="Doe",
            email="johnDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000000")
        storage.new(u)
        self.assertIn("User.{}".format(u.id), storage.all())
        self.assertEqual(storage.get("User", u.id), u)
        self.assertEqual(storage.get("User", "123456"), None)

    def test_count(self):
        """ Tests that the count method of the storage engine works """
        storage = Storage(test=True)
        storage.reload()
        u = User(
            first_name="John",
            last_name="Doe",
            email="johnDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000000")
        storage.new(u)
        u = User(
            first_name="Tony",
            last_name="Doe",
            email="tonyDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000001")
        storage.new(u)
        e = Event(
            name="Birthday",
            description="My birthday",
            event_type="public",
            start_time="2021-02-17T22:46:38.883037",
            end_time="2021-02-17T22:56:38.883037",
            location="San Francisco",
            host=u.id,
            price=0.00
            )
        storage.new(e)
        self.assertEqual(storage.count(), 3)

    def test_count_cls(self):
        """ Tests that the count method of the storage engine works """
        storage = Storage(test=True)
        storage.reload()
        u = User(
            first_name="John",
            last_name="Doe",
            email="johnDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000000")
        storage.new(u)
        u = User(
            first_name="Tony",
            last_name="Doe",
            email="tonyDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000001")
        storage.new(u)
        e = Event(
            name="Birthday",
            description="My birthday",
            event_type="public",
            start_time="2021-02-17T22:46:38.883037",
            end_time="2021-02-17T22:56:38.883037",
            location="San Francisco",
            host=u.id,
            price=0.00
            )
        storage.new(e)
        self.assertEqual(storage.count("User"), 2)
        self.assertEqual(storage.count("Event"), 1)

    def test_delete(self):
        """ Tests that the delete method of the storage engine works """
        storage = Storage(test=True)
        storage.reload()
        u1 = User(
            first_name="John",
            last_name="Doe",
            email="johnDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000000")
        storage.new(u1)
        u2 = User(
            first_name="Tony",
            last_name="Doe",
            email="tonyDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000001")
        storage.new(u2)
        e = Event(
            name="Birthday",
            description="My birthday",
            event_type="public",
            start_time="2021-02-17T22:46:38.883037",
            end_time="2021-02-17T22:56:38.883037",
            location="San Francisco",
            host=u1.id,
            price=0.00
            )
        storage.new(e)
        self.assertEqual(storage.count(), 3)
        storage.delete(u2)
        self.assertEqual(storage.count(), 2)
        self.assertNotIn("User.{}".format(u2.id), storage.all())
