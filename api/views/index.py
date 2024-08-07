#!/usr/bin/env python3
""" Base routes for the api """
from flasgger.utils import swag_from
from flask import (
    make_response,
    jsonify,
    redirect,
)

from api.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
@swag_from('documentation/indexes/status.yml')
def api_status():
    """ Returns the status of the API """
    return make_response(jsonify({'status': 'OK'}), 200)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
@swag_from('documentation/indexes/stats.yml')
def api_stats():
    """ Return relevant api stats """

    data = {
        'users': 'User',
        'events': 'Event',
    }
    db_stats = {}
    for key, value in data.items():
        db_stats[key] = storage.count(value)

    return make_response(jsonify(db_stats), 200)


@app_views.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    """ Returns the index form """
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Login Form</title>
    </head>
    <body>
    <h1>Hello Stranger!</h1>
    <form id="login-form">
        <input type="text" name="first_name" placeholder="first name">
        <input type="text" name="last_name" placeholder="last name">
        <input type="text" name="gender" placeholder="gender">
        <input type="text" name="date_of_birth" placeholder="dob">
        <input type="text" name="phone" placeholder="phone">
        <input type="text" name="email" placeholder="email">
        <input type="password" name="password" placeholder="password">
        <input type="submit" value="Create">
    </form>
    <script>
        document.getElementById("login-form").addEventListener(
        "submit",
        function(event) {
            event.preventDefault();
            const formElements = event.target.elements;
            const formData = {};
            for (const element of formElements) {
                if (element.name) {
                    formData[element.name] = element.value;
                }
            }
            // Send form data as JSON
            fetch("/app/users", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response from the server
                console.log("Cookies Set")
                console.log(data);
                alert(
                    'Browser logged in, you can now make requests in this window' + '\n' + data
                );
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    </script>
    </body>
    </html>
    """
