#!/usr/bin/env python3
""" Users route for database """
import jwt
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
from models.event import Event
from models.user import User
from api.auths.login import (
    login_required,
    current_user,
    current_app,
)


@app_views.route(
    '/events/<event_id>/attend',
    methods=['GET', 'POST', 'DELETE'],
    strict_slashes=False)
@login_required
@swag_from(
    'documentation/event_attendees/attend.yml',
    methods=['GET', 'POST', 'DELETE'])
def attend(event_id):
    """ adds the current user to the attendees """

    session = storage.Session()
    event = session.query(Event).filter(Event.id == event_id).one()

    if request.method == 'GET':
        if current_user.id == event.host:
            attendees = [user.to_dict() for user in event.attendees]
            session.close()
            return make_response(jsonify(attendees), 200)
        session.close()
        return make_response(jsonify({
            'message': 'You can only view attendees for your own events',
        }), 405)
    elif request.method == 'POST':
        if current_user.id == event.host:
            session.close()
            return make_response(
                jsonify({
                    'message': 'You do not need to attend your own event'
                }),
                405
            )
        if request.args.get('user_id'):
            event.attendees.append(
                storage.get('User', request.get('user_id')))
        else:
            if current_user.id in [user.id for user in event.attendees]:
                session.close()
                return make_response(jsonify({
                    'message': 'You are already attending {}'.format(
                        event.name
                    ),
                    'event': event.to_dict(),
                }), 201)
        event.attendees.append(storage.get('User', current_user.id))
        session.add(event)
        session.commit()
        session.close()
        return make_response(jsonify({
            'message': 'You are now attending {}'.format(event.name),
            'event': event.to_dict(),
        }), 201)
    elif request.method == 'DELETE':
        if current_user.id == event.host:
            session.close()
            abort(405, description='You cannot unattend your own event')
        if current_user.id not in [user.id for user in event.attendees]:
            session.close()
            abort(405, description='You are not attending this event')
        event.attendees.remove(storage.get('User', current_user.id))
        session.commit()
        session.close()
        return make_response(jsonify({
            'message': 'You are no longer attending {}'.format(event.name),
            'event': event.to_dict(),
        }), 202)
