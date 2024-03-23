import logging

from pydantic import Field
from core.settings.app import AppSettings
from core.settings.env import ENV_PATH, ENR_FILE
import os
from loguru import logger



 
class ProdAppSettings(AppSettings):
    debug: bool = True

    title: str = "Prod TemplateProject API"

    logging_level: int = logging.DEBUG  
    class Config(AppSettings.Config):
        env_file = ENR_FILE
