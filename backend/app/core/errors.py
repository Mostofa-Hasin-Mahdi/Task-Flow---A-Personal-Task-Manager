from typing import Any, Optional


class AppError(Exception):
    """Base application exception for all domain and operational errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class NotFoundError(AppError):
    """Exception raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=404, details=details)


class ValidationError(AppError):
    """Exception raised when business rule or input validation fails."""

    def __init__(self, message: str = "Validation failed", details: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=400, details=details)
