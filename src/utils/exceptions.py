"""
Custom exceptions for the Connected Vehicles API.
"""


class ProcessingError(Exception):
    """Raised when processing of data fails."""

    pass


class ValidationError(Exception):
    """Raised when data validation fails."""

    pass


class DynamoDBError(Exception):
    """Raised when DynamoDB operations fail."""

    pass
