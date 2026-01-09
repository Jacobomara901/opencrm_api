from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx

from opencrm.exceptions import AuthenticationError

if TYPE_CHECKING:
    pass


class AuthStrategy(ABC):
    @abstractmethod
    def apply_to_request(self, data: dict[str, str]) -> dict[str, str]:
        pass

    @abstractmethod
    def apply_to_headers(self, headers: dict[str, str]) -> dict[str, str]:
        pass


@dataclass
class APIKeyAuth(AuthStrategy):
    api_key: str
    pass_key: str

    def apply_to_request(self, data: dict[str, str]) -> dict[str, str]:
        return {**data, "apikey": self.api_key, "passkey": self.pass_key}

    def apply_to_headers(self, headers: dict[str, str]) -> dict[str, str]:
        return headers


@dataclass
class HeaderAuth(AuthStrategy):
    api_key: str
    pass_key: str

    def apply_to_request(self, data: dict[str, str]) -> dict[str, str]:
        return data

    def apply_to_headers(self, headers: dict[str, str]) -> dict[str, str]:
        return {**headers, "KEY1": self.api_key, "KEY2": self.pass_key}


@dataclass
class SessionAuth(AuthStrategy):
    access_key: str

    def apply_to_request(self, data: dict[str, str]) -> dict[str, str]:
        return {**data, "accesskey": self.access_key}

    def apply_to_headers(self, headers: dict[str, str]) -> dict[str, str]:
        return headers

    @classmethod
    def from_login(
        cls,
        base_url: str,
        api_key: str,
        pass_key: str,
        user_agent: str,
    ) -> "SessionAuth":
        login_url = f"{base_url}/api/rest/login"
        headers = {
            "User-Agent": user_agent,
            "Content-Type": "multipart/form-data",
        }

        try:
            response = httpx.post(
                login_url,
                data={"key": api_key, "passkey": pass_key},
                headers=headers,
                timeout=30.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise AuthenticationError(
                f"Login failed with status {e.response.status_code}",
                details={"response": e.response.text},
            ) from e
        except httpx.RequestError as e:
            raise AuthenticationError(
                f"Login request failed: {e}",
            ) from e

        try:
            access_key = response.json().get("accesskey") or response.text.strip()
        except Exception:
            access_key = response.text.strip()

        if not access_key:
            raise AuthenticationError(
                "Login succeeded but no access key returned",
                details={"response": response.text},
            )

        return cls(access_key=access_key)
