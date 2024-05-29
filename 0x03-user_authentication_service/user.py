#!/usr/bin/env python3
# Module creation of the user table database
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """_summary_
    Args:
        Base (_type_): _description_
    Returns:
        _type_: _description_
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    hashed_password = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """_summary_
        Returns:
            _type_: _description_
        """
        return f"<User(id={self.id}), email='{self.email}'>"
        # return "<User(id='%s', email='%s', hashed_password='%s')>" % (
        #     self.id, self.email, self.hashed_password)
