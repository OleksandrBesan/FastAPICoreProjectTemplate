from schemas.errors.base import BaseError
from pydantic import Field


class NotFoundIdentifier(BaseError):
    """
    The provided id does not exist in DB
    """

    common_description: str = "identifier does not exist"
    statusCode: int = Field(default=404, description=common_description)
    message: str = Field(
        default=common_description,
        description=common_description
    )
    responseType: str = Field(
        default="notFoundIdentifier", description=common_description
    )
