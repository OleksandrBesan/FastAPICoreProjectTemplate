import logging
import sys
from typing import Any, Dict, List, Tuple, NamedTuple
from loguru import logger
from pydantic import SecretStr, Field
from pydantic_settings import SettingsConfigDict
from core.logging import InterceptHandler
from core.settings.base import BaseAppSettings
import os


class LoggingRequestRestrictRoutesWithKeys(NamedTuple):
    routes: List[str] = ['*']
    filter_keys: List[str] = ['*']
    mask_keys: List[str] = ['*']


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "TemplateProject API"
    version: str = "2.0.0"
    secret_key: SecretStr = Field(default_factory=lambda: SecretStr(os.environ['SECRET_KEY']))
    api_prefix: str = "/api"
    jwt_token_prefix: str = "Token"
    allowed_hosts: List[str] = ["*"]
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    header_name_traceId: str = "traceId"
    logging_request_headers: List[str] = ["*"]
    logging_request_restrict_routes_with_keys: LoggingRequestRestrictRoutesWithKeys = LoggingRequestRestrictRoutesWithKeys()
    logging_response_filter: List[str] = ["*"]
    token_algorithm: str = "HS256"
    model_config = SettingsConfigDict(validate_assignment=True)
    DB_POSTGRESQL_URL_PARAMS:dict = {}
    DB_POSTGRESQL_MIN_CONNECTION:int = 5
    DB_POSTGRESQL_MAX_CONNECTION:int = 20

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

        fmt = "[{time}]|[{extra[tag]}]|[{extra[path]}]|[{extra[traceId]}][{level}]|[{name}:{function}:{line}] - [{message}]"
        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level, "format": fmt}],
                         extra={"traceId": "", "path": "", "tag": ""})
