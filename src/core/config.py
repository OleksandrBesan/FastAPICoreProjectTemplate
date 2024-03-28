from functools import lru_cache
from typing import Dict, Type

from core.settings.app import AppSettings
from core.settings.base import AppEnvTypes, BaseAppSettings
from core.settings.development import DevAppSettings
from core.settings.production import ProdAppSettings
from core.settings.test import TestAppSettings
from pydantic import SecretStr
import os


environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    secret_key = SecretStr(os.environ.get('SECRET_KEY', 'default_secret'))
    config = environments[app_env]
    return config(secret_key=secret_key)
