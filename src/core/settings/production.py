import logging
from core.settings.app import AppSettings
from core.settings.env import ENR_FILE
from pydantic import SecretStr, Field
import os


class ProdAppSettings(AppSettings):
    debug: bool = True
    title: str = "Prod TemplateProject API"
    secret_key: SecretStr = Field(default_factory=lambda: SecretStr(os.environ['SECRET_KEY']))
    logging_level: int = logging.DEBUG
    env_file: str = ENR_FILE
