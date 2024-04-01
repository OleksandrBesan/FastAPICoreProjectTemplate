import logging
import sys
from typing import Any, Dict, List, Tuple, NamedTuple
from loguru import logger
from pydantic import SecretStr, Field
from core.logging import InterceptHandler
from core.settings.base import BaseAppSettings
import os


class LoggingRequestRestrictRoutesWithKeys(NamedTuple):
    routes: List[str] = ['*']
    filter_keys: List[str] = ['*']
    mask_keys: List[str] = ['host']


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "TemplateProject API"
    version: str = "2.0.0"
    secret_key: SecretStr = Field(default_factory=lambda: os.environ['SECRET_KEY'])
    api_prefix: str = "/api"
    jwt_token_prefix: str = "Token"
    allowed_hosts: List[str] = ["*"]
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    header_name_requestId: str = "requestId"
    logging_request_headers: List[str] = ["*"]
    logging_request_restrict_routes_with_keys: LoggingRequestRestrictRoutesWithKeys = LoggingRequestRestrictRoutesWithKeys()
    logging_response_filter: List[str] = ["*"]

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_env(self) -> None:
        """
        configuring environments  from env stores
        """
        pass

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        fmt = "[{time}]|[{extra[tag]}]|[{extra[path]}]|[{extra[requestId]}][{level}]|[{name}:{function}:{line}] - [{message}]"
        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level, "format": fmt}],
                         extra={"requestId": "", "path": "", "tag": ""})
