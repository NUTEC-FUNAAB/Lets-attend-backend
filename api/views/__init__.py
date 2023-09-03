#!/usr/bin/python3
""" Blueprint for let'sattend api """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/')

from api.views.events import *  # noqa: E402
from api.views.event_attendees import *  # noqa: E402
from api.views.index import *  # noqa: E402
from api.views.users import *  # noqa: E402
