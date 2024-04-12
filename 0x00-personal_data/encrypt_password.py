#!/usr/bin/env python3
""" Encrypting passwords """

import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """This returns a salted, hashed password"""
    pd = password.encode()
    hashed = hashpw(pd, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password"""

    return bcrypt.checkpw(password.encode(), hashed_password)
