class AuthException(Exception):
    """Base exception for the Auth module."""

class InvalidCredentialsException(AuthException):
    def __init__(self):
        super().__init__("Invalid email or password")

class InvalidTokenException(AuthException):
    def __init__(self):
        super().__init__("Invalid authentication token")

class ExpiredTokenException(AuthException):
    def __init__(self):
        super().__init__("Authentication token has expired")