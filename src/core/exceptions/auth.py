from core.exceptions.base import BaseHTTPException
from models.errors.auth import InvalidTokenError, CreationTokenError


class InvalidTokenException(BaseHTTPException):
    model = InvalidTokenError
    statusCode = model.getStatusCodeDefault()
    message = model.getMessageDefault()


class CreationTokenException(BaseHTTPException):
    model = CreationTokenError
    statusCode = model.getStatusCodeDefault()
    message = model.getMessageDefault()
