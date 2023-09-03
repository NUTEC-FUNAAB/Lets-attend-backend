#!/usr/bin/env python3
""" Login methods module """
from api.auths import auth
from datetime import timedelta
from flask import (
    current_app,
    make_response,
    jsonify,
    request,
    abort,
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
)
from hashlib import md5
from models import storage
import jwt


@auth.route(
    '/login',
    methods=['POST'],
    strict_slashes=False)
def login():
    """ Logs a user in """
    try:
        credentials = request.get_json()
    except Exception:
        abort(401, 'Not the valid json')

    email = credentials.get('email')
    password = credentials.get('password')

    all_objs = storage.all('User')
    user = None
    for obj in all_objs.values():
        if obj.email == email:
            hash = md5()
            hash.update(password.encode("utf-8"))
            pass_hash = hash.hexdigest()
            if obj.password == pass_hash:
                user = obj
                break
            else:
                response = jsonify({'message': 'Incorrect Password'})
                return make_response(response, 401)
    if user:
        login_user(user, remember=True, duration=timedelta(days=30))
        token = jwt.encode(
            {'user_id': user.id},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

        user_dict = user.to_dict()
        user_dict['type'] = 'User'
        response = make_response(jsonify({'message': 'Login successful',
                                          'user': user_dict}), 200)
        response.set_cookie('token', token, httponly=False)
        return response
    else:
        return make_response(
            jsonify({'message': 'User with this email not found'}),
            404)


@auth.route('/logout')
@login_required
def logout():
    """ Logs a user out """
    logout_user()
    response = make_response(
        jsonify({'message': 'Logged out'}), 200)
    response.set_cookie('token', '', httponly=True)
    return response


@auth.route('/authenticaed')
def authorized():
    """ Checks if a user is logged in """
    if current_user.is_authenticated:
        user_dict = current_user.to_dict()
        user_dict['type'] = 'User'
        return make_response(
            jsonify({'authenticated': True, 'user': user_dict}),
            200)
    else:
        return make_response(
            jsonify({'authenticated': False}),
            200)
