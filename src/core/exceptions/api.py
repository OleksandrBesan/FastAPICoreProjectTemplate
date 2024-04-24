from core.exceptions.base import BaseHTTPException
from schemas.errors.api import BadRequestError, InternalServerError


class BadRequestException(BaseHTTPException):
    statusCode = BadRequestError.getStatusCodeDefault()
    message = BadRequestError.getMessageDefault()
    model = BadRequestError


class InternalServerException(BaseHTTPException):
    statusCode = InternalServerError.getStatusCodeDefault()
    message = InternalServerError.getMessageDefault()
    model = InternalServerError
