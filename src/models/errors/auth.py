from models.errors.base import BaseError
from pydantic import Field


class InvalidTokenError(BaseError):
    """
    The provided token is invalid or expired
    """
    common_description: str = "token is invalid or expired"
    statusCode: int = Field(default=401, description=common_description)
    message: str = Field(default=common_description, description=common_description)
    responseType: str = Field(default="invalidToken", description=common_description)


class CreationTokenError(BaseError):
    """
    This error occurs when there is an internal error while creating token
    """
    common_description: str = "An internal server error occurred."
    statusCode: int = Field(default=500, description=common_description)
    message: str = Field(default=common_description, description=common_description)
    responseType: str = Field(default="creationTokenError", description=common_description)
