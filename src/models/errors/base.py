from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class BaseError(BaseModel):
    statusCode: int = Field(default=500, description="HTTP status code")
    responseType: str = Field(default="InternalServerException", description="The type of error")
    message: str = Field(default="Internal Server Error", description="main shor message of exception")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="The timestamp when the error occurred")
    isError: bool = Field(default=True, description="Flag indicating this is an error response")
    requestId: str = Field(default_factory=lambda: str(uuid.uuid4()), description="A unique identifier for this particular instance of the error and request. Default is uuid, but should use requestID from Headers.")

    @classmethod
    def getStatusCodeDefault(cls):
        return cls.__fields__['statusCode'].default

    @classmethod
    def getResponseTypeExceptionDefault(cls):
        return cls.__fields__['responseType'].default

    @classmethod
    def getMessageDefault(cls):
        return cls.__fields__['message'].default
