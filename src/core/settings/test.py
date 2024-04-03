import logging
from core.settings.app import AppSettings
from core.settings.env import ENR_FILE
from pydantic import SecretStr, Field
import os


class TestAppSettings(AppSettings):
    debug: bool = True
    title: str = "Test TemplateProject API"
    secret_key: SecretStr = Field(default_factory=lambda: SecretStr(os.environ['SECRET_KEY']))
    logging_level: int = logging.DEBUG
    LOCALSTACK_URL: str = "http://{localstack_host}:{localstack_port}".format(localstack_host="localhost", localstack_port=4566)
    env_file: str = ENR_FILE
