from pymongo.errors import PyMongoError


class RedBabyError(PyMongoError):
    """
    Generic error.
    """


class DocumentNotFound(RedBabyError):
    """
    Raised when no document is found.
    """


class ClientNotFoundError(Exception):
    def __init__(self, details: str = ""):
        self.details = details
        super().__init__(f"Redbaby Client not found. Details: {self.details}")


class ConnectionNotFoundError(Exception):
    def __init__(self, details: str = ""):
        self.details = details
        super().__init__(f"Redbaby Connection not found. Details: {self.details}")
