from core.security.tokens.base import BaseIssuer
from core.config import get_app_settings
from core.exceptions.auth import InvalidTokenException, CreationTokenNotSupportedException, AuthProviderInternalException
from loguru import logger
from typing import Any, Dict
import jwt
import json
from datetime import timedelta
from core.settings.app import AppSettings
from cachetools import TTLCache
from threading import Lock
import requests

jwks_cache: TTLCache[Any, Any] = TTLCache(maxsize=10, ttl=86400)
cache_lock = Lock()


class OuterIssuer(BaseIssuer):

    def __init__(self, setting: AppSettings = get_app_settings()) -> None:
        self.setting = get_app_settings
        super().__init__()

    def set_jwks(self, jwks_url: str):
        self.jwks_url_provider = jwks_url

    def get_jwks(self, from_source : bool = False):
        with cache_lock:
            if 'jwks' in jwks_cache and not from_source:
                return jwks_cache['jwks']
            try:
                response = requests.get(self.jwks_url_provider)
                response.raise_for_status()
                jwks = response.json()
                jwks_cache['jwks'] = jwks
                return jwks
            except requests.RequestException as e:
                logger.error(f"An error occurred while fetching JWKS: {e}")
                raise AuthProviderInternalException()

    def createToken(self, subject: str | Any, expires_delta: timedelta) -> str:
        raise CreationTokenNotSupportedException()

    def decodeToken(self, token) -> Dict:
        header = jwt.get_unverified_header(token)
        keys = self.get_jwks()['keys']
        for key in keys:
            if key['kid'] == header['kid']:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
                decoded_token = jwt.decode(token, public_key, algorithms=['RS256'])
                return decoded_token
        raise InvalidTokenException()


class CognitoIssuer(OuterIssuer):

    def __init__(self, setting: AppSettings = get_app_settings()) -> None:
        self.setting = get_app_settings
        region_name = getattr(self.setting, 'AWS_DEFAULT_REGION', 'us-east-1')
        user_pool_id = getattr(self.setting, 'COGNITO_USER_POOL_ID', None)
        self.jwks_url_provider = f'https://cognito-idp.{region_name}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'
        super().__init__()
