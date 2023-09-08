#!/usr/bin/env python3
""" Users route for database """
from datetime import timedelta
from flask import (
    abort,
    jsonify,
    make_response,
    request,
)
from flasgger.utils import swag_from

from api.views import app_views
from models import storage
from models.user import User
from api.auths.login import (
    login_required,
    login_user,
    logout_user,
    current_user,
    current_app,
)


@app_views.route(
    '/users/<user_id>/events',
    methods=['GET'],
    strict_slashes=False,
)
@login_required
@swag_from('documentation/users/user_events.yml', methods=['GET'])
def user_events(user_id):
    """ a user's events """
    session = storage.Session()
    user = session.query(User).filter(User.id == user_id).one()
    events = [event.to_dict() for event in user.my_events]
    session.close()
    response = make_response(jsonify(events), 200)
    return response


@app_views.route(
    '/users/events',
    methods=['GET'],
    strict_slashes=False,
)
@login_required
@swag_from('documentation/users/current_user_events.yml', methods=['GET'])
def my_events():
    """ gets all events for the current user """
    session = storage.Session()
    user = session.query(User).filter(User.id == current_user.id).one()
    events = [event.to_dict() for event in user.my_events]
    session.close()
    response = make_response(jsonify(events), 200)
    return response
