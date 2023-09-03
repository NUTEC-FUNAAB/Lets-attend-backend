#!/usr/bin/python3
""" Event class for handling events """
import enum

from sqlalchemy import (
    Table,
    DECIMAL,
    Enum,
    String,
    Column,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from models.base import (
    BaseModel,
    Base,
)


event_attendees = Table(
    "event_attendees",
    Base.metadata,
    Column(
        "event_id",
        String(40),
        ForeignKey("events.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "user_id",
        String(40),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class Event(BaseModel, Base):
    """ Event class """

    __tablename__ = "events"

    name = Column(
        String(45),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=False
    )

    event_type = Column(
        String(8),
        default='public',
        nullable=False
    )

    start_time = Column(
        DateTime,
        nullable=False
    )

    end_time = Column(
        DateTime,
        nullable=False
    )

    location = Column(
        String(255),
        nullable=False
    )

    host = Column(
        String(40),
        ForeignKey("users.id"),
        nullable=False
    )

    price = Column(
        DECIMAL(10, 2),
        default=0.00,
        nullable=False
    )

    attendees = relationship(
        "User",
        secondary=event_attendees,
        back_populates="my_events",
    )
