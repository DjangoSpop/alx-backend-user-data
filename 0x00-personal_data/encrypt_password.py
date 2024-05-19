#!/usr/bin/env python3
"""Module for password encryption and validation."""
import bcrypt
...


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): Password to be hashed.

    Returns:
        bytes: Hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a password against a hashed password.

    Args:
        hashed_password (bytes): Hashed password.
        password (str): Password to be validated.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
