#!/usr/bin/env python3
""" Module for testing the base model """
import datetime
import unittest
import pep8 as pycodestyle

from models.base import BaseModel


class TestBase(unittest.TestCase):
    """ Tests the base class """

    def test_pep8_conformance(self):
        """ Test that models/base.py conforms to PEP8. """

        for path in ['models/base.py',
                     'tests/test_models/test_base.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_init(self):
        """ tests the initialization """

        b = BaseModel()
        self.assertTrue(hasattr(b, "id"))
        self.assertTrue(hasattr(b, "created_at"))

    def test_id(self):
        """ Tests the id """
        b = BaseModel()
        self.assertTrue(type(b.id), str)
        b = BaseModel()
        self.assertEqual(len(b.id), 36)
        b = BaseModel()
        self.assertNotEqual(b.id, BaseModel().id)

    def test_created_at(self):
        """ Tests the created at attribute """
        b = BaseModel()
        self.assertIsInstance(b.created_at, datetime.datetime)
        c = BaseModel()
        self.assertTrue(b.created_at != c.created_at)

    def test_to_dict(self):
        """ Tests the to_dict method """
        b = BaseModel()
        self.assertIsInstance(b.to_dict(), dict)
        self.assertIn('created_at', b.to_dict())

    def test_kwargs(self):
        """ Test the keyword arguments """

        b = BaseModel(
            id="123456",
            created_at="2021-02-17T22:46:38.883037",
            )
        self.assertNotEqual(b.id, "123456")
        self.assertNotEqual(b.created_at, "2021-02-17T22:46:38.883037")
