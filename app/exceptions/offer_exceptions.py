class OfferException(Exception):
    """Base class for all event-related exceptions."""

class OfferNotFound(OfferException):
    """Raised when no Offer is found."""