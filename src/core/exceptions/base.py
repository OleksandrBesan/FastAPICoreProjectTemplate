from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status as statuscode
from schemas.errors.base import BaseError
from typing import Union


class BaseHTTPException(HTTPException):
    """Base error for custom API any HTTP exceptions"""
    message = "internal server error"
    statusCode = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError
    responseType = "InternalServerException"

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        kwargs.setdefault("statusCode", self.statusCode)
        kwargs.setdefault("responseType", self.responseType)
        self.message = kwargs["message"]
        self.statusCode = kwargs["statusCode"]
        self.responseType = kwargs["responseType"]
        self.status_code = self.statusCode
        self.data = self.model(message=self.message, statusCode=self.statusCode, responseType=self.responseType)

    def __str__(self):
        return self.message

    def response(self, traceId: Union[str, None]):
        self.data.traceId = traceId
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.statusCode
        )

    @classmethod
    def response_model(cls):
        return {cls.statusCode: {"model": cls.model}}
