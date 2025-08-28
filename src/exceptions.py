#!/usr/bin/env python3
"""Custom exceptions for the clause mate extraction script."""


class ClauseMateExtractionError(Exception):
    """Base exception for clause mate extraction errors."""


class ParseError(ClauseMateExtractionError):
    """Raised when parsing fails."""

    def __init__(
        self,
        message: str,
        line_number: int | None = None,
        raw_data: str | None = None,
    ):
        """Initialize the ParseError.

        Args:
            message: Error message.
            line_number: Line number where the error occurred.
            raw_data: Raw data that caused the error.
        """
        self.line_number = line_number
        self.raw_data = raw_data

        if line_number is not None:
            message = f"Line {line_number}: {message}"
        if raw_data is not None:
            message = f"{message} (Raw data: {raw_data[:100]}...)"

        super().__init__(message)


class ValidationError(ClauseMateExtractionError):
    """Raised when validation fails."""


class FileProcessingError(ClauseMateExtractionError):
    """Raised when file processing fails."""


class CoreferenceExtractionError(ClauseMateExtractionError):
    """Raised when coreference extraction fails."""
