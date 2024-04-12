#!/usr/bin/env python3
""" Encrypting passwords """

import bcrypt
from bcript import hashpw


def hash_password(password: str) -> bytes:
    """This returns a salted, hashed password"""
    pwd = password.encode()
    hashed = hashpw(pwd, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password"""

    return bcrypt.checkpw(password.encode(), hashed_password)
