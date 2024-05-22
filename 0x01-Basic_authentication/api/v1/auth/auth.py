#!/usr/bin/env python3
"""Module to manage authentication."""
from typing import List, TypeVar
from flask import request 
import flask


class Auth:
    """Class to manage the API authentication."""
    
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
        """Authorize the request."""
        pass

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user."""
        pass
    def session_cookie(self, request=None):
        """Session cookie."""
        if request is None or "session_id" not in request.cookies:
            return None
        return request.cookies["session_id"]
    