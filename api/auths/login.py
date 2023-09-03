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

    user = storage.lookup(email)
    if not user:
        return make_response(
            jsonify({'message': 'User with this email not found'}),
            404)

    hash = md5()
    hash.update(password.encode("utf-8"))
    pass_hash = hash.hexdigest()
    if user.password != pass_hash:
        response = jsonify({'message': 'Incorrect Password'})
        return make_response(response, 401)
    else:
        login_user(user, remember=True, duration=timedelta(days=30))
        token = jwt.encode(
            {'user_id': user.id},
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

        user_dict = user.to_dict()
        response = make_response(jsonify({'message': 'Login successful',
                                          'user': user_dict}), 200)
        response.set_cookie('token', token, httponly=False)
        return response


@auth.route('/logout')
@login_required
def logout():
    """ Logs a user out """
    logout_user()
    response = make_response(
        jsonify({'message': 'Logged out'}), 200)
    response.set_cookie('token', '', httponly=True)
    return response


@auth.route('/authenticated')
def authorized():
    """ Checks if a user is logged in """
    if current_user.is_authenticated:
        user_dict = current_user.to_dict()
        return make_response(
            jsonify({'authenticated': True, 'user': user_dict}),
            200)
    else:
        return make_response(
            jsonify({'authenticated': False}),
            200)
