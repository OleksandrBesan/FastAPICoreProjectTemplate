from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status as statuscode
from models.errors.base import BaseError
from typing import Union


class BaseHTTPException(HTTPException):
    """Base error for custom API any HTTP exceptions"""
    message = "internal server error"
    code = statuscode.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError
    typeException = "InternalServerException"

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        kwargs.setdefault("code", self.code)
        kwargs.setdefault("typeException", self.typeException)
        self.message = kwargs["message"]
        self.code = kwargs["code"]
        self.typeException = kwargs["typeException"]
        self.status_code = self.code
        self.data = self.model(message=self.message, code=self.code, typeException=self.typeException)

    def __str__(self):
        return self.message

    def response(self, requestId: Union[str, None]):
        self.data.requestId = requestId
        return JSONResponse(
            content=self.data.dict(),
            status_code=self.code
        )

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}
