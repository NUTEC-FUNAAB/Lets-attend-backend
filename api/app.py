#!/usr/bin/env python3
""" Main routes for the api """
from dotenv.main import load_dotenv
from flasgger import Swagger
from flasgger.utils import swag_from
from flask import (
    Flask,
    render_template,
    make_response,
    jsonify,
)
from flask_cors import CORS
from flask_login import LoginManager
from os import environ

from api.views import app_views
from api.auths import auth
from models import storage


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

login_manager = LoginManager(app)

CORS(
    auth,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

app.register_blueprint(app_views)
app.register_blueprint(auth)

cors = CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)


@login_manager.user_loader
def load_user(user_id):
    """ Retrieves a user by id """
    user = storage.get('User', user_id)
    if user is not None:
        return user


@app.teardown_appcontext
def close_db(err):
    """ Closes the storage session on an error """
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """
        Returns 404 Error For unidentified route
    ---
    responses:
      200:
        description: A successful response
        examples:
            404: "Not Found"
    """
    response = make_response(jsonify({'Error': 'Not found'}), 404)
    return response


contact = '{"Name": "Aina Jesulayomi", "Email": "jesulayomi081@gmail.com" }'
app.config['SWAGGER'] = {
    'title': "Let's Attend API",
    'uiversion': 2,
    'version': '0.1.0',
    'description': "API for Let's Attend",
    'termsOfService': "Contact Developers for Terms of Service",
    'contact': contact
}

Swagger(app)


if __name__ == "__main__":
    app.run(
        host=environ.get('ATTEND_HOST', default='0.0.0.0'),
        port=environ.get('ATTEND_PORT', default='5050'),
        threaded=True)
