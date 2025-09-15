"""
Custom exceptions for the application.
"""

class TaskManagementException(Exception):
    """Base exception for task management system."""

class NotFoundError(TaskManagementException):
    """Raised when a requested resource is not found."""

class DuplicateError(TaskManagementException):
    """Raised when trying to create a duplicate resource."""

class ValidationError(TaskManagementException):
    """Raised when validation fails."""

class PermissionError(TaskManagementException):
    """Raised when user doesn't have permission to perform action."""

