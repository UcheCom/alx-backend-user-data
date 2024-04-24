#!/usr/bin/env python3
""" Module is SessionDBAuth class
"""
from flask import request
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """ This creates and stores new instance of UserSession
        """
        session_id = super().create_session(user_id)
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the user_id by requesting UserSession
        """

        if not session_id:
            return None
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return None
        if self.session_duration <= 0:
            return None
        creation_dur = user_sessions[0].created_at + \
            timedelta(seconds=self.session_duration)
        if creation_dur < datetime.utcnow():
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the session Id
        """
        if not request:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        UserSession.get(user_id).remove()
        return True
