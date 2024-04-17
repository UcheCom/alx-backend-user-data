#!/usr/bin/env python3
"""Module to manage the API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class manages authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method defines the required authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """ Method used to create the authentication header
        Return:
          - String
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Method defines the current user"""
        return None
