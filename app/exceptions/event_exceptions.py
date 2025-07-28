class EventException(Exception):
    """Base class for all event-related exceptions."""

class EventNotFound(EventException):
    """Raised when no Event is found."""