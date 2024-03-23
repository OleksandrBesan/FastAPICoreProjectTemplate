import logging

from pydantic import Field
from core.settings.app import AppSettings
from core.settings.env import ENV_PATH, ENR_FILE
import os
from loguru import logger


 
class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Test TemplateProject API"

    logging_level: int = logging.DEBUG   
    LOCALSTACK_URL: str = "http://{localstack_host}:{localstack_port}".format(localstack_host="localhost",localstack_port=4566)

    class Config(AppSettings.Config):
        env_file = ENR_FILE
