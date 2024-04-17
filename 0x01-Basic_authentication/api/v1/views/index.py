#!/usr/bin/env python3
""" This module handles index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """This GETs /api/v1/status
    Return: the status of the API
    """
    return jsonify({"status": 'OK'})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """This GETs /api/v1/stats
    Return: the number of objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """This GETs /api/v1/unathorized
    Return: an error message
    """
    abort(401, description='Unauthorized')
