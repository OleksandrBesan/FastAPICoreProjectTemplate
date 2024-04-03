from enum import Enum
from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from core.settings.env import ENV_PATH
import os


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = Field(default_factory=lambda: AppEnvTypes[os.environ.get('ENV', 'prod')])
    secret_key: SecretStr = Field(default_factory=lambda: SecretStr(os.environ['SECRET_KEY']))
    env: str = Field(default_factory=lambda: os.environ['ENV'])
    env_file: str = ENV_PATH
    model_config = SettingsConfigDict(extra="allow")
