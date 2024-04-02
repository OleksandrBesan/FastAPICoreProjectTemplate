from fastapi import Request
from fastapi.exceptions import RequestValidationError
from models.errors.base import BaseError
from core.utils.requestId import getRequestId
from typing import List, Tuple, Type, Callable
from core.exceptions.base import BaseHTTPException

errorHandlers: List[Tuple[Type[Exception], Callable]] = []


async def http_exception_handler(request: Request, exc: BaseHTTPException):
    requestId = getRequestId(request)
    response = exc.response(requestId)
    return response


async def validation_exception_handler(request: Request, exc: Exception):
    requestId = getRequestId(request)
    error_response = BaseError(statusCode=422, message=str(exc), responseType="ValidationException", requestId=requestId)
    return error_response


errorHandlers.append((BaseHTTPException, http_exception_handler))
errorHandlers.append((RequestValidationError, validation_exception_handler))
