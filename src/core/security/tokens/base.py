from abc import abstractmethod
from typing import Dict, Any
from datetime import timedelta


class BaseIssuer:
    @abstractmethod
    def createToken(self, subject: str | Any, expires_delta: timedelta) -> str:
        pass

    @abstractmethod
    def decodeToken(self, token: Any) -> Dict:
        pass
