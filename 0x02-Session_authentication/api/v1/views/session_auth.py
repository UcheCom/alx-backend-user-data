#!/usr/bin/env python3
""" This is view to handle all routes for the Session authentication
"""
import os
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request
from api.v1.auth.session_auth import SessionAuth


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login() -> str:
    """POST /api/v1/auth_session/login
    Return: a JSON
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            sess_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            sess_name = os.getenv('SESSION_NAME')
            resp.set_cookie(sess_name, sess_id)
            return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """ DELETE api/v1/auth_session/logout
    Return: a JSON
    """
    from api.v1.app import auth
    delected = auth.destroy_session(request)
    if not delected:
        abort(404)
    return jsonify({}), 200
