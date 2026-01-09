from typing import Any, Literal

import httpx

from opencrm.auth import APIKeyAuth, AuthStrategy, HeaderAuth, SessionAuth
from opencrm.exceptions import (
    APIError,
    ConfigurationError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
)

DEFAULT_USER_AGENT = "opencrm-python/0.1.0"
DEFAULT_TIMEOUT = 30.0


class HTTPClient:
    def __init__(
        self,
        system_name: str,
        auth: AuthStrategy,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._base_url = f"https://{system_name}.opencrm.co.uk/api/rest"
        self._auth = auth
        self._user_agent = user_agent
        self._timeout = timeout
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                timeout=self._timeout,
                headers={"User-Agent": self._user_agent},
            )
        return self._client

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> "HTTPClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "User-Agent": self._user_agent,
            "Content-Type": "multipart/form-data",
        }
        return self._auth.apply_to_headers(headers)

    def _build_data(self, data: dict[str, Any]) -> dict[str, str]:
        str_data = {k: str(v) for k, v in data.items() if v is not None}
        return self._auth.apply_to_request(str_data)

    def _handle_response(self, response: httpx.Response) -> Any:
        if response.status_code == 404:
            raise NotFoundError(
                "Resource not found",
                status_code=404,
                response_body=response.text,
            )

        if response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded",
                status_code=429,
                response_body=response.text,
            )

        if response.status_code >= 400:
            raise APIError(
                f"API request failed",
                status_code=response.status_code,
                response_body=response.text,
            )

        if not response.text:
            return None

        try:
            return response.json()
        except Exception:
            return response.text

    def request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self._base_url}/{endpoint}"
        headers = self._build_headers()
        request_data = self._build_data(data or {})

        try:
            response = self.client.request(
                method=method,
                url=url,
                data=request_data if request_data else None,
                params=params,
                headers=headers,
            )
        except httpx.RequestError as e:
            raise ConnectionError(f"Request failed: {e}") from e

        return self._handle_response(response)

    def get(self, endpoint: str, **kwargs: Any) -> Any:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> Any:
        return self.request("POST", endpoint, **kwargs)


class OpenCRMClient:
    def __init__(
        self,
        system_name: str,
        api_key: str,
        pass_key: str,
        auth_method: Literal["keys", "headers", "session"] = "keys",
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        if not system_name:
            raise ConfigurationError("system_name is required")
        if not api_key or not pass_key:
            raise ConfigurationError("api_key and pass_key are required")

        self._system_name = system_name
        self._user_agent = user_agent
        self._timeout = timeout

        auth: AuthStrategy
        if auth_method == "keys":
            auth = APIKeyAuth(api_key=api_key, pass_key=pass_key)
        elif auth_method == "headers":
            auth = HeaderAuth(api_key=api_key, pass_key=pass_key)
        elif auth_method == "session":
            base_url = f"https://{system_name}.opencrm.co.uk"
            auth = SessionAuth.from_login(base_url, api_key, pass_key, user_agent)
        else:
            raise ConfigurationError(f"Invalid auth_method: {auth_method}")

        self._http = HTTPClient(
            system_name=system_name,
            auth=auth,
            user_agent=user_agent,
            timeout=timeout,
        )

    @property
    def http(self) -> HTTPClient:
        return self._http

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "OpenCRMClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
