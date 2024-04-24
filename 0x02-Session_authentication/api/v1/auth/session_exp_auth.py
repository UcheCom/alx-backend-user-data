#!/usr/bin/env python3
""" Session Expiration auth class"""
import os
from flask import request
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication class with expiration"""

    def __init__(self):
        """init method"""
        if not os.getenv('SESSION_DURATION') or not \
            int(os.getenv('SESSION_DURATION')):
            self.session_duration = 0

        self.session_duration = int(os.getenv('SESSION_DURATION'))

    def create_session(self, user_id: str = None) -> str:
        """This creates a session_id based on user_id"""
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        sess_dict = {}
        sess_dict['user_id'] = user_id
        sess_dict['created_at'] = datetime.now()
        self.user_id_by_session_id[sess_id] = sess_dict

        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Thsi returns the user_id based on the session_id"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return sess_dict['user_id']
        sess_dict = self.user_id_by_session_id[session_id]
        if "craeted_at" not in sess_dict:
            return None
        current_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sess_dict['created_at'] + time_span
        if exp_time < current_time:
            return None
        return self.sess_dict["user_id"]
