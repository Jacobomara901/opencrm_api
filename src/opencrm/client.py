"""
OpenCRM API Client.

This module provides the main client interface for interacting with the OpenCRM REST API.

Example:
    >>> from opencrm import OpenCRMClient
    >>> client = OpenCRMClient(
    ...     system_name="yoursystem",
    ...     api_key="your-api-key",
    ...     pass_key="your-pass-key",
    ... )
    >>> leads = client.leads.list()
    >>> client.close()

Using as context manager:
    >>> with OpenCRMClient(system_name="test", api_key="key", pass_key="pass") as client:
    ...     contacts = client.contacts.list()
"""

from typing import TYPE_CHECKING, Any, Literal

import httpx

from opencrm.auth import APIKeyAuth, AuthStrategy, HeaderAuth, SessionAuth
from opencrm.exceptions import (
    APIError,
    ConfigurationError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
)

if TYPE_CHECKING:
    from opencrm.resources.companies import CompaniesResource
    from opencrm.resources.contacts import ContactsResource
    from opencrm.resources.helpdesk import HelpdeskResource
    from opencrm.resources.leads import LeadsResource
    from opencrm.resources.opportunities import OpportunitiesResource
    from opencrm.resources.products import ProductsResource
    from opencrm.resources.projects import ProjectsResource

DEFAULT_USER_AGENT = "opencrm-python/0.1.0"
DEFAULT_TIMEOUT = 30.0


class HTTPClient:
    """
    Low-level HTTP client for OpenCRM API requests.

    Handles authentication, request building, and response parsing.
    Most users should use OpenCRMClient instead of this class directly.

    Args:
        system_name: Your OpenCRM system name (the subdomain part of your URL).
        auth: Authentication strategy to use.
        user_agent: Custom User-Agent header. Defaults to "opencrm-python/0.1.0".
            Note: OpenCRM blocks default curl user agents.
        timeout: Request timeout in seconds. Defaults to 30.0.
    """

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
    """
    Main client for interacting with the OpenCRM API.

    Provides access to all OpenCRM resources (leads, contacts, companies, etc.)
    through a simple, Pythonic interface.

    Args:
        system_name: Your OpenCRM system name (subdomain). For example, if your
            OpenCRM URL is "acme.opencrm.co.uk", use "acme".
        api_key: Your OpenCRM API key. Contact OpenCRM support to obtain this.
        pass_key: Your OpenCRM API pass key. Contact OpenCRM support to obtain this.
        auth_method: Authentication method to use. Options:
            - "keys" (default): Pass API keys with each request
            - "headers": Pass API keys as HTTP headers (KEY1/KEY2)
            - "session": Login once and use session access key
        user_agent: Custom User-Agent string. Defaults to "opencrm-python/0.1.0".
            Important: OpenCRM blocks default curl user agents.
        timeout: Request timeout in seconds. Defaults to 30.0.

    Raises:
        ConfigurationError: If required parameters are missing or invalid.
        AuthenticationError: If session authentication fails (auth_method="session").

    Example:
        >>> client = OpenCRMClient(
        ...     system_name="acme",
        ...     api_key="ABC123",
        ...     pass_key="XYZ789",
        ... )
        >>> # List all leads
        >>> leads = client.leads.list()
        >>> # Get a specific contact
        >>> contact = client.contacts.get(crmid=12345)
        >>> # Create a new company
        >>> new_id = client.companies.create(
        ...     accountname="New Corp",
        ...     assigned_user_id=1,
        ... )
        >>> client.close()

    Note:
        Always call close() when done, or use as a context manager:
        >>> with OpenCRMClient(...) as client:
        ...     leads = client.leads.list()
    """

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

    @property
    def leads(self) -> "LeadsResource":
        from opencrm.resources.leads import LeadsResource

        if not hasattr(self, "_leads"):
            self._leads = LeadsResource(self._http)
        return self._leads

    @property
    def contacts(self) -> "ContactsResource":
        from opencrm.resources.contacts import ContactsResource

        if not hasattr(self, "_contacts"):
            self._contacts = ContactsResource(self._http)
        return self._contacts

    @property
    def companies(self) -> "CompaniesResource":
        from opencrm.resources.companies import CompaniesResource

        if not hasattr(self, "_companies"):
            self._companies = CompaniesResource(self._http)
        return self._companies

    @property
    def projects(self) -> "ProjectsResource":
        from opencrm.resources.projects import ProjectsResource

        if not hasattr(self, "_projects"):
            self._projects = ProjectsResource(self._http)
        return self._projects

    @property
    def helpdesk(self) -> "HelpdeskResource":
        from opencrm.resources.helpdesk import HelpdeskResource

        if not hasattr(self, "_helpdesk"):
            self._helpdesk = HelpdeskResource(self._http)
        return self._helpdesk

    @property
    def opportunities(self) -> "OpportunitiesResource":
        from opencrm.resources.opportunities import OpportunitiesResource

        if not hasattr(self, "_opportunities"):
            self._opportunities = OpportunitiesResource(self._http)
        return self._opportunities

    @property
    def products(self) -> "ProductsResource":
        from opencrm.resources.products import ProductsResource

        if not hasattr(self, "_products"):
            self._products = ProductsResource(self._http)
        return self._products

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "OpenCRMClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
