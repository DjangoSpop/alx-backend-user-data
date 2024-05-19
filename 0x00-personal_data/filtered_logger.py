#!/usr/bin/env python3
"""
Module for filtering and obfuscating personal data
"""
import re
import logging
import mysql.connector
from mysql.connector import error
import os
from typing import List
import bcrypt

# Define the PII fields to be obfuscated
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates the specified fields in the given message.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String to use for obfuscation.
        message (str): Log message to be obfuscated.
        separator (str): Separator used in the log message.

    Returns:
        str: Obfuscated log message.
    """
    pattern = r"|".join(rf"({field})=[^{separator}]*" for field in fields)
    return re.sub(pattern, lambda match: f"{match.group(1)}={redaction}", message)

class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        return filter_datum(self.fields, self.REDACTION, super().format(record), self.SEPARATOR)

def get_logger() -> logging.Logger:
    """
    Returns a Logger object configured for obfuscating PII data.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a MySQL connection object.
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    try:
        connector = mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=db_name
        )
        return connector
    except error.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def main():
    """
    Main function that retrieves and displays user data.
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = "; ".join([f"{field}={value}" for field, value in zip(cursor.column_names, row)])
        logger.info(message)
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
    