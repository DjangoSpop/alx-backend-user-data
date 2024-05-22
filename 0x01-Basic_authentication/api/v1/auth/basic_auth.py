import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
 
class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header:str) -> str:
        """Extract base64 authorization header."""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decode base64 authorization header."""
        if base64_authorization_header is None or type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None
    def extract_user_credentials(self, decode_base64_authorization_header: str) -> (str, str):
        """Extract user credentials."""
        if decode_base64_authorization_header is None or type(decode_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decode_base64_authorization_header:
            return (None, None)
        if ':' not in decode_base64_authorization_header:
            return (None, None)
        if decode_base64_authorization_header.count(':') > 1:
            user_email, *user_pwd = decode_base64_authorization_header.split(':', 1)
            user_pwd = ':'.join(user_pwd)
        else:
            user_email, user_pwd = decode_base64_authorization_header.split(':', 1)
        return (user_email, user_pwd)
        return tuple(decode_base64_authorization_header.split(':', 1))
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """User object from credentials."""
        if user_email is None or user_pwd is None or type(user_email) is not str or type(user_pwd) is not str:
            return None
        try:
            user = User()
            user.email = user_email
            user.password = user_pwd
            return user
        except Exception:
            return None
    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request."""
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        decoded_header = self.decode_base64_authorization_header(base64_authorization_header)
        user_credentials = self.extract_user_credentials(decoded_header)
        user_email, user_pwd = user_credentials
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
    
    