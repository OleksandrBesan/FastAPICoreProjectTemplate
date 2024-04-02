from pydantic import BaseModel
from models.responseBase import BaseResponse


class SomeRequestModel(BaseModel):
    """
   Model Request for some endpoint
    """
    text: str
    id: int


class SomeResponseModel(BaseResponse):
    """
    Response model with some result
    """
    result: bool
