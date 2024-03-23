from fastapi import  Request 
from core.config import get_app_settings

def getRequestId(request: Request):
    settings = get_app_settings()
    return request.headers.get(settings.header_name_requestId)
