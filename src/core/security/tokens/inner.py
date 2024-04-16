from core.security.tokens.base import BaseIssuer
from core.config import get_app_settings
from core.exceptions.auth import InvalidTokenException, CreationTokenException
from loguru import logger
from typing import Any, Dict
import jwt
from datetime import datetime, timedelta, UTC
from core.settings.app import AppSettings


class InnerIssuer(BaseIssuer):

    def __init__(self, setting: AppSettings = get_app_settings()) -> None:
        self.setting = setting
        super().__init__()

    def createToken(self, subject: str | Any, expires_delta: timedelta) -> str:
        try:
            expire = datetime.now(UTC) + expires_delta
            to_encode = {"exp": expire, "sub": str(subject)}
            encoded_jwt = jwt.encode(to_encode, self.setting.secret_key.get_secret_value(), algorithm=self.setting.token_algorithm)
            return encoded_jwt
        except (jwt.exceptions.DecodeError, AttributeError) as e:
            logger.error("Error creating token:", e)
            raise CreationTokenException()

    def decodeToken(self, token: str) -> Dict:
        try:
            token_info = jwt.decode(token, self.setting.secret_key.get_secret_value(), algorithms=[self.setting.token_algorithm])
            return token_info
        except (jwt.exceptions.DecodeError, AttributeError) as e:
            logger.error("Error decoding token:", e)
            raise InvalidTokenException()
