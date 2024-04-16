import pytest
from datetime import timedelta
from core.security.tokens.inner import InnerIssuer
from core.exceptions.auth import InvalidTokenException, CreationTokenException
from core.config import get_app_settings, AppEnvTypes
from pydantic import Field
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
setting = get_app_settings()


def test_token_creation_and_decoding(monkeypatch, capsys):
    test_secret_key = 'test'
    monkeypatch.setenv('SECRET_KEY', test_secret_key)
    subject = "test_user"
    expires_delta = timedelta(hours=1)
    issuer = InnerIssuer()
    token = issuer.createToken(subject, expires_delta)
    assert token is not None, "Failed to create token"
    decoded = issuer.decodeToken(token)
    with capsys.disabled():
        print(f"Token: {token}")
        print(f"Decoded: {decoded}")
    assert decoded['sub'] == subject, "Token decoding failed: subject mismatch"


class SomeBaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = Field(default_factory=lambda: AppEnvTypes[os.environ.get('ENV', 'prod')])
    secret_key: str = Field(default_factory=lambda: os.environ['SECRET_KEY'])
    model_config = SettingsConfigDict(extra="allow")


def test_token_creation_failure():
    mock_settings = SomeBaseAppSettings()
    issuer = InnerIssuer(mock_settings)
    with pytest.raises(CreationTokenException):
        issuer.createToken("test_subject", timedelta(hours=1))


def test_token_decoding_failure():
    issuer = InnerIssuer()
    invalid_token = "invalid.token.string"
    with pytest.raises(InvalidTokenException):
        issuer.decodeToken(invalid_token)
