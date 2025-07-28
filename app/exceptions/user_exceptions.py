class UserException(Exception):
    """Base class for all User-related exceptions."""

class UserAlreadyExists(UserException):
    """Raised when user's email is already in use."""