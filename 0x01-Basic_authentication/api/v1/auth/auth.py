from typing import List, TypeVar
from flask import rquest 
import flask


class Auth:
    """Auth class to manage the API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication for some paths."""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True
      
        

    def authorization_header(self, request=None) -> str:
        """Authorization header."""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user."""
        return None
    def session_cookie(self, request=None):
        """Session cookie."""
        if request is None or "session_id" not in request.cookies:
            return None
        return request.cookies["session_id"]
    