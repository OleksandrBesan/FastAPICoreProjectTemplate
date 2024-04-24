from schemas.errors.base import BaseError
from pydantic import Field


class BadRequestError(BaseError):
    statusCode: int = Field(default=400, description="Bad Request")
    message: str = Field(default="Bad Request", description="Bad Request")
    responseType: str = Field(default="apiException", description="The type of error apiException")


class InternalServerError(BaseError):
    statusCode: int = Field(default=500, description="Internal Server Error")
    message: str = Field(default="Internal Server Error", description="Internal Server Error")
    responseType: str = Field(default="apiException", description="The type of error apiException")
