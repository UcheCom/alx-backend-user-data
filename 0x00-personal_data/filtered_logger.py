#!/usr/bin/env python3
"""Regex-ing"""

import logging
import re
from os import environ
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "password", "phone", "ssn")


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


def get_logger() -> logging.Logger:
    """This returns logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """This returns a connector to the database"""
    db_name = environ.get('PERSONAL_DATA_DB_NAME')
    host = environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    username = environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = environ.get('PERSONAL_DATA_DB_PASSWORD', '')
    conn = mysql.connector.connection.MySQLConnection(db=db_name,
                                                      password=passwd,
                                                      host=host,
                                                      user=username)
    return conn


def main():
    """The main entry point"""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        str_row = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(str_row.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
