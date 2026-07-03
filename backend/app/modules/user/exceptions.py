from uuid import UUID

class UserException(Exception):
    """Base exception for the User module."""

class UserNotFoundException(UserException):
    """Raised when a user cannot be found."""

    def __init__(self, user_id: UUID | None = None, email: str | None = None):
        if user_id is not None:
            message = f"User with id '{user_id}' not found."
        elif email is not None:
            message = f"User with email '{email}' not found."
        else:
            message = "User not found."

        super().__init__(message)

class UserAlreadyExistsException(UserException):
    """Raised when attempting to create a user that already exists."""

    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists.")

class UserInactiveException(UserException):
    """Raised when an operation requires an active user."""

    def __init__(self):
        super().__init__("User is inactive.")

class UserInactiveException(UserException):
    """Raised when an operation requires an active user."""

    def __init__(self):
        super().__init__("User is inactive.")

class InvalidUserDataException(UserException):
    """Raised when user data is invalid."""

    def __init__(self):
        super().__init__("Invalid user data.")