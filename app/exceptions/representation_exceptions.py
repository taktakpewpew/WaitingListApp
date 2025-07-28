class RepresentationException(Exception):
    """Base class for all representation-related exceptions."""

class RepresentationNotFound(RepresentationException):
    """Raised when no Representation is found."""