import logging

from core.settings.app import AppSettings
from core.settings.env import ENV_PATH
from pydantic import SecretStr, Field
import os


class DevAppSettings(AppSettings):
    debug: bool = True
    title: str = "Dev TemplateProject API"
    logging_level: int = logging.DEBUG
    secret_key: SecretStr = Field(default_factory=lambda: SecretStr(os.environ['SECRET_KEY']))
    env_file: str = ENV_PATH
