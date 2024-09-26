from http import HTTPStatus
from typing import Optional, List, Dict


class HaruException(Exception):
    """Base exception class for the Haru framework."""


class HTTPException(HaruException):
    """Base class for HTTP exceptions."""

    def __init__(self, status_code: int, description: Optional[str] = None, headers: Optional[Dict[str, str]] = None):
        self.status_code = status_code
        self.description = description or HTTPStatus(status_code).phrase
        self.headers = headers or {}
        super().__init__(f"{status_code} {self.description}")


class BadRequest(HTTPException):
    """400 Bad Request"""

    def __init__(self, description: Optional[str] = None):
        super().__init__(HTTPStatus.BAD_REQUEST, description)


class Unauthorized(HTTPException):
    """401 Unauthorized"""

    def __init__(self, description: Optional[str] = None):
        super().__init__(HTTPStatus.UNAUTHORIZED, description)


class Forbidden(HTTPException):
    """403 Forbidden"""

    def __init__(self, description: Optional[str] = None):
        super().__init__(HTTPStatus.FORBIDDEN, description)


class NotFound(HTTPException):
    """404 Not Found"""

    def __init__(self, description: Optional[str] = None):
        super().__init__(HTTPStatus.NOT_FOUND, description)


class MethodNotAllowed(HTTPException):
    """405 Method Not Allowed"""

    def __init__(self, allowed_methods: List[str], description: Optional[str] = None):
        headers = {'Allow': ', '.join(sorted(allowed_methods))}
        super().__init__(HTTPStatus.METHOD_NOT_ALLOWED, description, headers)
        self.allowed_methods = allowed_methods


class InternalServerError(HTTPException):
    """500 Internal Server Error"""

    def __init__(self, description: Optional[str] = None):
        super().__init__(HTTPStatus.INTERNAL_SERVER_ERROR, description)
