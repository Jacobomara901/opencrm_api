"""Custom exceptions for the OpenCRM API client."""

from typing import Any


class OpenCRMError(Exception):
    """Base exception for all OpenCRM errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class AuthenticationError(OpenCRMError):
    """Raised when authentication fails."""

    pass


class APIError(OpenCRMError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: Any = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, details)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.response_body:
            parts.append(f"Response: {self.response_body}")
        return " | ".join(parts)


class RateLimitError(APIError):
    """Raised when the API rate limit is exceeded."""

    pass


class NotFoundError(APIError):
    """Raised when a requested resource is not found."""

    pass


class ValidationError(OpenCRMError):
    """Raised when request data fails validation."""

    pass


class ConfigurationError(OpenCRMError):
    """Raised when the client is misconfigured."""

    pass


class ConnectionError(OpenCRMError):
    """Raised when connection to the API fails."""

    pass
