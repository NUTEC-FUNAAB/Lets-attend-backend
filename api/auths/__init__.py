#!/usr/bin/env python3
""" Passes the auth view to the blueprint """
from flask import Blueprint


auth = Blueprint('auth', __name__, url_prefix='/api/')


from api.auths.login import *   # noqa: E402
