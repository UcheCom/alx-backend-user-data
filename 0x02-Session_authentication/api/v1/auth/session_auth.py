#!/usr/bin/env python3
"""First step for creating a new session authentication mechanism"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4
from typing import TypeVar


class SessionAuth(Auth):
    """Session Auth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Method creates a Session ID for a user with id user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        sess_id = str(uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User id based on a session_id
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar("User"):
        """ Returns a User instance based on a cookie value
        """
        sess_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None) -> bool:
        """ This deletes the user session
        """
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_id = self.user_id_for_session_id(sess_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[sess_id]
        return True
