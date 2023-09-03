#!/usr/bin/env python3
""" Module for testing the user """
import unittest
import pep8 as pycodestyle

from datetime import datetime
from hashlib import md5

from models.base import BaseModel
from models.user import User


class TestBase(unittest.TestCase):
    """ Tests the usr class """

    def test_pep8_conformance(self):
        """ Test that models/user.py conforms to PEP8. """

        for path in ['models/user.py',
                     'tests/test_models/test_user.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_init(self):
        """ tests the initialization """

        u = User()
        self.assertTrue(hasattr(u, "id"))
        self.assertTrue(hasattr(u, "created_at"))

    def test_id(self):
        """ Tests the id """
        u = User()
        self.assertTrue(type(u.id), str)
        u = User()
        self.assertEqual(len(u.id), 36)
        u = User()
        self.assertNotEqual(u.id, User().id)

    def test_created_at(self):
        """ Tests the created at attribute """
        u = User()
        self.assertIsInstance(u.created_at, datetime)
        c = User()
        self.assertTrue(u.created_at != c.created_at)

    def test_to_dict(self):
        """ Tests the to_dict method """
        u = User()
        self.assertIsInstance(u.to_dict(), dict)
        self.assertIn('created_at', u.to_dict())

    def test_kwargs(self):
        """ Test the keyword arguments """

        u = User(
            id="123456",
            created_at="2021-02-17T22:46:38.883037",
            )
        self.assertNotEqual(u.id, "123456")
        self.assertNotEqual(u.created_at, "2021-02-17T22:46:38.883037")
        u = User(
            first_name="John",
            last_name="Doe",
            email="johnDdoe@gmail.com",
            password="password",
            gender='male',
            date_of_birth="2021-02-17T22:46:38.883037",
            phone="2348000000000")
        self.assertEqual(u.first_name, "John")
        self.assertIn('first_name', u.to_dict())
        self.assertIsInstance(u.password, str)
        self.assertTrue(u.password != "password")

    def test_password(self):
        """ Test the password attribute """

        u = User(password="password")
        self.assertIsInstance(u.password, str)
        self.assertTrue(u.password != "password")
        self.assertEqual(
            u.password,
            md5("password".encode('utf-8')).hexdigest()
        )

    def test_email(self):
        """ Test the email attribute """

        with self.assertRaises(ValueError):
            u = User(email="johnDdoe")
        u = User(email="johnDdoe@gmail.com")
        self.assertIsInstance(u.email, str)

    def test_first_name(self):
        """ test the first or last names """

        with self.assertRaises(ValueError):
            u = User(first_name="John1")
        u = User(first_name="John")
        self.assertIsInstance(u.first_name, str)
