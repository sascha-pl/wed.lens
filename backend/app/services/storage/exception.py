class StorageError(Exception):
    """Base exception for storage operations."""


class StorageObjectNotFoundError(StorageError):
    """Raised when a requested storage object does not exist."""


class StorageObjectAlreadyExistsError(StorageError):
    """Raised when attempting to create an object that already exists."""