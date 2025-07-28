class WaitingListException(Exception):
    """Base class for all waiting list-related exceptions."""

class WaitingListNotFound(WaitingListException):
    """Raised when requested WaitingList was not found."""

class TicketsStillAvailable(WaitingListException):
    """Raised when inventory still has stock — waiting list should not be used."""

class AlreadyInWaitingList(WaitingListException):
    """Raised when user is already on the waiting list for this offer/representation."""

class RepresentationEventAndOfferEventDontMatch(WaitingListException):
    """Raised when provided representation_id and offer_id dont match the same event."""