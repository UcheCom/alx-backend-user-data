#!/usr/bin/env python3
"""Regex-ing"""

import logging
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """This is init method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ This filters value in incomming log records """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted
