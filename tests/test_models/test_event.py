#!/usr/bin/env python3
""" Module for testing the user """
import unittest
import pep8 as pycodestyle

from datetime import datetime

from models.base import BaseModel
from models.user import User
from models.event import Event


class TestBase(unittest.TestCase):
    """ tests the event class """

    def test_pep8_conformance(self):
        """ Test that models/event.py conforms to PEP8. """

        for path in ['models/event.py',
                     'tests/test_models/test_event.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_init(self):
        """ tests the initialization """

        e = Event()
        self.assertTrue(hasattr(e, "id"))
        self.assertTrue(hasattr(e, "created_at"))

    def test_id(self):
        """ Tests the id """
        e = Event()
        self.assertTrue(type(e.id), str)
        e = Event()
        self.assertEqual(len(e.id), 36)
        e = Event()
        self.assertNotEqual(e.id, Event().id)

    def test_created_at(self):
        """ Tests the created at attribute """
        e = Event()
        self.assertIsInstance(e.created_at, datetime)
        c = Event()
        self.assertTrue(e.created_at != c.created_at)

    def test_to_dict(self):
        """ Tests the to_dict method """
        e = Event()
        self.assertIsInstance(e.to_dict(), dict)
        self.assertIn('created_at', e.to_dict())

    def test_kwargs(self):
        """ Test the keyword arguments """

        e = Event(
            id="123456",
            created_at="2021-02-17T22:46:38.883037",
            )
        self.assertNotEqual(e.id, "123456")
        self.assertNotEqual(e.created_at, "2021-02-17T22:46:38.883037")
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
        self.assertEqual(e.name, "Birthday")
        self.assertEqual(e.host, u.id)
        self.assertIn('event_type', e.to_dict())
