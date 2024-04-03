from core.config import get_app_settings
from core.exceptions.auth import InvalidTokenException, CreationTokenException
from loguru import logger
from typing import Any, Dict
import jwt
from datetime import datetime, timedelta, UTC
from core.settings.app import AppSettings


def createToken(subject: str | Any, expires_delta: timedelta, setting: AppSettings = get_app_settings()) -> str:
    try:
        expire = datetime.now(UTC) + expires_delta
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, setting.secret_key.get_secret_value(), algorithm=setting.token_algorithm)
        return encoded_jwt
    except (jwt.exceptions.DecodeError, AttributeError) as e:
        logger.error("Error creating token:", e)
        raise CreationTokenException()


def decodeToken(token, setting: AppSettings = get_app_settings()) -> Dict:
    try:
        token_info = jwt.decode(token, setting.secret_key.get_secret_value(), algorithms=[setting.token_algorithm])
        return token_info
    except (jwt.exceptions.DecodeError, AttributeError) as e:
        logger.error("Error decoding token:", e)
        raise InvalidTokenException()
