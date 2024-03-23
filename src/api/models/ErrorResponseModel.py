from pydantic import BaseModel 

class ErrorResponseModel(BaseModel):
    error_code: int
    error_message: str
