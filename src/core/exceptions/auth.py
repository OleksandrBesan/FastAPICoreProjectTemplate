from core.exceptions.base import BaseHTTPException
from schemas.errors.auth import InvalidTokenError, CreationTokenError, CreationTokenNotSupportedError, AuthProviderInternalError


class InvalidTokenException(BaseHTTPException):
    model = InvalidTokenError
    statusCode = model.getStatusCodeDefault()
    message = model.getMessageDefault()


class CreationTokenException(BaseHTTPException):
    model = CreationTokenError
    statusCode = model.getStatusCodeDefault()
    message = model.getMessageDefault()


class CreationTokenNotSupportedException(BaseHTTPException):
    model = CreationTokenNotSupportedError
    statusCode = model.getStatusCodeDefault()
    message = model.getMessageDefault()


class AuthProviderInternalException(BaseHTTPException):
    model = AuthProviderInternalError
    statusCode = model.getStatusCodeDefault()
    message = model.getMessageDefault()
