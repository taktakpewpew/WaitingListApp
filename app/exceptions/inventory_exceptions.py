class InventoryException(Exception):
    """Base class for all inventory-related exceptions."""

class InventoryNotFound(InventoryException):
    """Raised when no inventory is found for offer/representation."""