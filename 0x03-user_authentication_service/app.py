#!/usr/bin/env python3
"""Basic flask app
"""

from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index() -> str:
    """This index route
    Return: The home page
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """This posts/registers new users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """This Posts a login info"""
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email. password):
        abort(401)

    session_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
