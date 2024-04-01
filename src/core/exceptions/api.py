from core.exceptions.base import BaseHTTPException
from models.errors.api import BadRequestError, InternalServerError


class BadRequestException(BaseHTTPException):
    code = BadRequestError.getCodeDefault()
    message = BadRequestError.getMessageDefault()
    model = BadRequestError


class InternalServerException(BaseHTTPException):
    code = InternalServerError.getCodeDefault()
    message = InternalServerError.getMessageDefault()
    model = InternalServerError
