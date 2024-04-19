#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract the Base64 part of the Authorization header
        Return: The Base64 part of the header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[-1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Decode a Base64-encoded string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64_str = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(base64_str)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ This extracts user email and password
        Return: (email, password)
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email = decoded_base64_authorization_header.split(':')[0]
        passwd = decoded_base64_authorization_header[len(email) + 1:]
        return (email, passwd)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns a User instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        This returns a User instance based on a received request
        """
        try:
            Auth_header = self.authorization_header(request)
            base64_str = self.extract_base64_authorization_header(Auth_header)
            decoded = self.decode_base64_authorization_header(base64_str)
            email, passwd = self.extract_user_credentials(decoded)
            user = self.user_object_from_credentials(email, passwd)
            return user
        except Exception:
            return None
