#!/usr/bin/python3
""" User class for hosts and attendees """
import enum

from email_validator import validate_email
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy import (
    Enum,
    String,
    Column,
    DateTime,
)
from sqlalchemy.orm import relationship
from typing import Any

from models.base import (
    BaseModel,
    Base,
)


class User(BaseModel, UserMixin, Base):
    """ User class """

    __tablename__ = "users"

    first_name = Column(
        String(45),
        nullable=False
    )

    last_name = Column(
        String(45),
        nullable=False
    )

    gender = Column(
        String(8),
        default='male',
        nullable=False
    )

    date_of_birth = Column(
        DateTime,
        nullable=False
    )

    email = Column(
        String(320),
        nullable=False,
        unique=True
    )

    phone = Column(
        String(20),
        unique=True
    )

    password = Column(
        String(64),
        nullable=False
    )

    my_events = relationship(
        "Event",
        secondary="event_attendees",
        back_populates="attendees",
        passive_deletes='all'
    )

    def __setattr__(self, name: str, value: Any) -> None:
        """ Sets attributes for the user class """

        if name == "first_name" or name == "last_name":
            if not value.isalpha():
                raise ValueError("Names must contain only letters")

        if name == "email":
            try:
                validate_email(value)
            except Exception:
                raise ValueError("Email address is invalid")

        if name == "password":
            md5_hash = md5()
            md5_hash.update(value.encode("utf-8"))
            value = md5_hash.hexdigest()

        super().__setattr__(name, value)
