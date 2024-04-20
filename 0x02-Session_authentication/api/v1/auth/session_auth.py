#!/usr/bin/env python3
"""First step for creating a new authentication mechanism"""
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session Auth class"""

