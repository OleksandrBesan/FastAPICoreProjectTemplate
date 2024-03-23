from enum import Enum
from pydantic import Field
from pydantic_settings import BaseSettings 
from core.settings.env import  ENV_PATH, ENR_FILE
import os


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"

class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = Field(default_factory=lambda: AppEnvTypes[os.environ.get('ENV', 'prod')])
    secret_key: str = Field(default_factory=lambda: os.environ['SECRET_KEY'])  
    env: str = Field(default_factory=lambda: os.environ['ENV'])   
    class Config:
        env_file = ENV_PATH
        extra = "allow"
        