#!/usr/bin/env python3
"""Regex-ing"""

import re
from typing import List


# PII_FIELDS = ("name", "email", "password", "phone", "ssn")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """This returns the log message obfuscated"""
    for field in fields:
        message = re.sub("{}=.*?{}".format(field, separator),
                         "{}={}{}".format(field, redaction, separator),
                         message)
    return message
