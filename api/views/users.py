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
from models.user import User
from api.auths.login import (
    login_required,
    login_user,
    logout_user,
    current_user,
    current_app,
)


@app_views.route(
    '/users',
    methods=['GET'],
    strict_slashes=False
)
@login_required
@swag_from('documentation/users/getusers.yml')
def all_users():
    """
        Configures GET method for the users route
    """
    all_users = storage.all(User)
    return make_response(jsonify(
        [user.to_dict() for user in all_users.values()]
    ), 200)


@app_views.route(
    '/users',
    methods=['POST', 'DELETE'],
    strict_slashes=False
)
@swag_from('documentation/users/newuser.yml', methods=['POST'])
@swag_from('documentation/users/deluser.yml', methods=['DELETE'])
def create_user():
    """ Creates a new user or signs a user up """
    if request.method == 'DELETE':
        logout_user()
        storage.delete(storage.get('User', current_user.id))
        return make_response(
            jsonify({'message': 'User Deleted and Logged out'}), 202)
    if not request.get_json():
        abort(400, description='Not a valid JSON dict')
    required = [
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'email',
        'password',
    ]
    for param in required:
        if param not in request.get_json():
            abort(
                406,
                description='Missing required parameter: {}'.format(param)
                )
    data = request.get_json()
    instance = User(**data)
    try:
        storage.new(instance)
    except Exception:
        return make_response(
            jsonify({'message': 'User already exists or invalid data'}),
            409
        )
    storage.save()
    login_user(instance, remember=True, duration=timedelta(days=30))
    token = jwt.encode(
            {'user_id': instance.id},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')
    user_data = instance.to_dict()
    response = make_response(
        jsonify(
            {
                'message': 'User created and logged in',
                'user': user_data,
                }), 201)
    response.set_cookie('token', token, httponly=False)
    return response


@app_views.route(
    '/users/<user_id>',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False
)
@login_required
@swag_from('documentation/users/getuser.yml', methods=['GET'])
@swag_from('documentation/users/moduser.yml', methods=['PUT'])
@swag_from('documentation/users/fastdeluser.yml', methods=['DELETE'])
def user(user_id):
    """ Operations involving a specific user """

    if request.method == 'GET':
        user = storage.get('User', user_id)
        if not user:
            abort(404, description='User not found')
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == 'PUT':
        if not request.get_json():
            abort(400, description='Not a valid JSON')
        ignore = ['id', 'created_at']
        data = request.get_json()
        user = storage.get('User', user_id)
        if not user:
            abort(404, description='User not found')
        for key, value in data.items():
            if key not in ignore:
                setattr(user, key, value)
        storage.new(user)
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == 'DELETE':
        user = storage.get('User', user_id)
        if not user:
            abort(404, description='User not found')
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({'Error': 'Method not allowed'}), 405)
