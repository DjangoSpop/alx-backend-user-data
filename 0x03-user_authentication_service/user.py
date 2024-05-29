#!/usr/bin/env python3
"""Module creation of the user table database"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User class for database table 'users'

    Args:
        Base (declarative_base): Base class for declarative SQLAlchemy class
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    hashed_password = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """String representation of User instance

        Returns:
            str: User instance representation
        """
        return "<User(id='{}', email='{}', hashed_password='{}')>".format(
            self.id, self.email, self.hashed_password
        )
