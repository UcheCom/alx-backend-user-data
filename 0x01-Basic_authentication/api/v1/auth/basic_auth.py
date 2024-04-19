#!/usr/bin/env python3
"""
Definition of class BasicAuth
"""
import base64
from api.v1.auth.auth import Auth


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
