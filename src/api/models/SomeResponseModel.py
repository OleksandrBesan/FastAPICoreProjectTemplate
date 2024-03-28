from pydantic import BaseModel


class SomeResponseModel(BaseModel):
    """
    Response model with some result
    """
    result: bool
