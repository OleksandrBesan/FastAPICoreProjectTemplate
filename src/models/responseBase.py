from pydantic import BaseModel, Field
from datetime import datetime, UTC
import uuid


class BaseResponse(BaseModel):
    statusCode: int = Field(default=200, description="HTTP status code")
    responseType: str = Field(default="success", description="The type of response")
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat(), description="The timestamp when the error occurred")
    isError: bool = Field(default=False, description="Flag indicating this is an usual response")
    requestId: str = Field(default_factory=lambda: str(uuid.uuid4()), description="A unique identifier for this particular instance of the error and request. Default is uuid, but should use requestID from Headers.")

    @classmethod
    def getStatusCodeDefault(cls):
        return cls.model_fields['statusCode'].default

    @classmethod
    def getResponseTypeExceptionDefault(cls):
        return cls.model_fields['responseType'].default