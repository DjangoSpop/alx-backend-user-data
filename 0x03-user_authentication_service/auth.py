#!/usr/bin/env python3
import uuid
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import NoResultFound
from db import DB

def _hash_password(password: str) -> bytes:
    """_summary_

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """    
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
class Auth:
    """_summary_ Auth class to interact with authntication
    database
    """    
    def __init__(self):
        self._db = DB()
    def register_user(self, email: str, password: str) -> User:
        """_summary_

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            User: _description_
        """        
        if self._db.find_user_by(email=email):
            raise ValueError("User {} already exists".format(email))
        return self._db.add_user(email, _hash_password(password))
    
    
    def create_session(self, email: str) -> str:
        try:
             user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = str(uuid.uuid4())
        self._db.update_user(user.id, session_id=session_id)
        return session_id
    
    
    def valid_login(self, email: str, password: str) -> bool:
        try:
            user = self._db.find_user_by(email=email)
            password_bytes = password.encode() if isinstance(password, str) else password
            hashed_password_bytes = user.hashed_password.encode() if isinstance(user.hashed_password, str) else user.hashed_password
            return bcrypt.checkpw(password_bytes, hashed_password_bytes)
        except NoResultFound:
            return False
        
    def get_reset_password_token(self, email: str) -> str:
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token = reset_token)
        return reset_token
    
    def update_password(self, reset_token: str, password: str) -> None:
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token = None)
