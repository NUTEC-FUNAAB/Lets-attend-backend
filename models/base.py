#!/usr/bin/env python3
""" The base class to inherit for other classes """

from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
)
from sqlalchemy.orm import declarative_base
from typing import (
    Dict,
    Any,
)
from uuid import uuid4


Base = declarative_base()


class BaseModel:
    """ The base class for all db classes """

    id = Column(
        String(40),
        primary_key=True,
        nullable=False,
        unique=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow().isoformat(),
        nullable=False
    )

    def __init__(self, **kwargs):
        """ Initializes the basemodel class  """

        if kwargs:
            for key, value in kwargs.items():
                if key not in ["id", "created_at"]:
                    setattr(self, key, value)

        self.id = str(uuid4())
        self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """ Returns the dictionary representation of the implied class """

        self_dict = self.__dict__.copy()
        for key in self_dict.keys():
            if key == "created_at":
                self_dict[key] = self.created_at.isoformat()
            if key == "attendees":
                self_dict[key] = [user.to_dict() for user in self_dict[key]]

        if "password" in self_dict:
            del self_dict["password"]
        if "_sa_instance_state" in self_dict:
            del self_dict["_sa_instance_state"]

        return self_dict
