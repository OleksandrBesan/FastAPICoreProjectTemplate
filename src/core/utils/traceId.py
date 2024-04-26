from fastapi import Request
from core.config import get_app_settings
from core.settings.app import AppSettings


class TraceIdExtractor:
    def __init__(self, request: Request, settings: AppSettings = get_app_settings()):
        self.request = request
        self.settings = settings

    def getTraceId(self):
        return self.request.headers.get(self.settings.header_name_traceId)
