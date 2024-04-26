from fastapi import Request
from fastapi.exceptions import RequestValidationError
from schemas.errors.base import BaseError
from core.utils.traceId import TraceIdExtractor
from typing import List, Tuple, Type, Callable
from core.exceptions.base import BaseHTTPException

errorHandlers: List[Tuple[Type[Exception], Callable]] = []


async def http_exception_handler(request: Request, exc: BaseHTTPException):
    traceId = TraceIdExtractor(request).getTraceId()
    response = exc.response(traceId)
    return response


async def validation_exception_handler(request: Request, exc: Exception):
    traceId = TraceIdExtractor(request).getTraceId()
    error_response = BaseError(statusCode=422, message=str(exc), responseType="ValidationException", traceId=traceId)
    return error_response


errorHandlers.append((BaseHTTPException, http_exception_handler))
errorHandlers.append((RequestValidationError, validation_exception_handler))
