#!/usr/bin/env python3
"""Module to manage the API authentication"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Class manages authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method defines the required authentication"""
        if path is None:
            return True

        elif excluded_paths is None or excluded_paths == []:
            return True

        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method used to create the authentication header
        Return:
          - String
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Method defines the current user"""
        return None

    def session_cookie(self, request=None):
        """Nethod returns a cookie value from a request
        """
        if not request:
            return None
        sess_name = os.getenv("SESSION_NAME")
        return request.cookies.get("_my_session_id")
