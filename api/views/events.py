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
        '/events',
        methods=['GET', 'POST'],
        strict_slashes=False)
@login_required
@swag_from('documentation/events/allevents.yml', methods=['GET'])
@swag_from('documentation/events/newevent.yml', methods=['POST'])
def all_events():
    """ Retrieves all events """

    if request.method == 'GET':
        event_dict = storage.all('Event')
        resp = make_response(jsonify([
            event.to_dict() for event in event_dict.values()
        ]), 200)
        return resp
    elif request.method == 'POST':
        data = request.get_json()
        requirements = [
            'name',
            'description',
            'start_time',
            'end_time',
            'location',
        ]
        for field in requirements:
            if field not in data.keys():
                abort(401, description='Missing Required parameter')
        data['host'] = current_user.id
        event = Event(**data)
        user = storage.get('User', current_user.id)
        event.attendees.append(user)
        storage.new(event)
        resp = make_response(jsonify({
            'message': 'Event Createtd',
            'event': event.to_dict()
            }), 201)
        return resp
    else:
        return make_response(jsonify({'message': 'Method not allowed'}), 405)


@app_views.route(
        '/events/<event_id>',
        methods=['GET', 'PUT', 'DELETE'],
        strict_slashes=False)
@login_required
@swag_from(
    'documentation/events/delevent.yml',
    methods=['DELETE'])
@swag_from(
    'documentation/events/getevent.yml',
    methods=['GET'])
@swag_from(
    'documentation/events/modevent.yml',
    methods=['PUT'])
def event_manager(event_id):
    """ Handlesevent methods """
    if request.method == 'GET':
        event = storage.get('Event', event_id)
        return make_response(
            jsonify({'event': event.to_dict()}), 200
        )
    elif request.method == 'PUT':
        data = request.get_json()
        event = storage.get('Event', event_id)
        for key, value in data.items():
            if key != 'id' and key != 'created_at':
                setattr(event, key, value)
            storage.new(event)
            return make_response(jsonify(event.to_dict()), 200)
    elif request.method == 'DELETE':
        event = storage.get('Event', event_id)
        storage.delete(event)
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({'message': 'Method not allowed'}), 405)
