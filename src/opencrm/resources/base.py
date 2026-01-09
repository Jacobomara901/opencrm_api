"""
Base resource class for OpenCRM API modules.

All resource classes (LeadsResource, ContactsResource, etc.) inherit from BaseResource.
"""

from typing import TYPE_CHECKING, Any, Generic, Iterator, TypeVar

from opencrm.models.base import CRMRecord, PaginationParams
from opencrm.utils.query import QueryBuilder

if TYPE_CHECKING:
    from opencrm.client import HTTPClient

T = TypeVar("T", bound=CRMRecord)


class BaseResource(Generic[T]):
    """
    Base class for all OpenCRM resource handlers.

    Provides standard CRUD operations and iteration for any OpenCRM module.
    Subclasses define the specific endpoints for each module.

    All resource methods accept either a QueryBuilder or raw query string for filtering.
    """

    _module_name: str = ""
    _list_endpoint: str = ""
    _count_endpoint: str = ""
    _get_endpoint: str = ""
    _edit_endpoint: str = ""
    _model_class: type[T]

    def __init__(self, http: "HTTPClient") -> None:
        self._http = http

    def _parse_list_response(self, response: Any) -> list[dict[str, Any]]:
        if isinstance(response, list):
            return response
        if isinstance(response, dict):
            return [response]
        return []

    def count(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
    ) -> int:
        """
        Count records matching the given criteria.

        Args:
            query: Filter criteria. Can be a QueryBuilder instance or raw query string
                in format "FIELDNAME|OPERATOR|VALUE".
            keywords: Full-text search keywords.

        Returns:
            Number of matching records.

        Example:
            >>> count = client.leads.count(query=query().equals("leadstatus", "New"))
            >>> print(f"Found {count} new leads")
        """
        data: dict[str, Any] = {}

        if query:
            query_str = query.build() if isinstance(query, QueryBuilder) else query
            if query_str:
                data["query_string"] = query_str

        if keywords:
            data["keywords"] = keywords

        result = self._http.post(self._count_endpoint, data=data)

        if isinstance(result, int):
            return result
        if isinstance(result, str) and result.isdigit():
            return int(result)
        return 0

    def list(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
        limit_start: int | None = None,
        limit_end: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        List records with optional filtering and pagination.

        Args:
            query: Filter criteria. Can be a QueryBuilder instance or raw query string.
            keywords: Full-text search keywords.
            limit_start: Start index for pagination (0-based).
            limit_end: End index for pagination.

        Returns:
            List of record dictionaries. Each dict contains field names as keys.

        Example:
            >>> # Get first 50 leads
            >>> leads = client.leads.list(limit_start=0, limit_end=50)
            >>> # Filter by status
            >>> new_leads = client.leads.list(query=query().equals("leadstatus", "New"))
        """
        data: dict[str, Any] = {}

        if query:
            query_str = query.build() if isinstance(query, QueryBuilder) else query
            if query_str:
                data["query_string"] = query_str

        if keywords:
            data["keywords"] = keywords
        if limit_start is not None:
            data["limit_start"] = limit_start
        if limit_end is not None:
            data["limit_end"] = limit_end

        response = self._http.post(self._list_endpoint, data=data)
        return self._parse_list_response(response)

    def get(self, crmid: int) -> dict[str, Any]:
        """
        Retrieve a single record by its CRM ID.

        Args:
            crmid: The unique OpenCRM record ID.

        Returns:
            Dictionary containing all record fields.

        Raises:
            NotFoundError: If the record doesn't exist.

        Example:
            >>> contact = client.contacts.get(crmid=12345)
            >>> print(contact["firstname"], contact["lastname"])
        """
        response = self._http.post(self._get_endpoint, data={"crmid": crmid})
        if isinstance(response, dict):
            return response
        return {}

    def create(self, **fields: Any) -> int:
        """
        Create a new record.

        Args:
            **fields: Field values to set on the new record. Use API field names.
                You should always include 'assigned_user_id' to set the record owner.

        Returns:
            The CRM ID of the newly created record.

        Example:
            >>> new_id = client.leads.create(
            ...     firstname="John",
            ...     lastname="Doe",
            ...     email="john@example.com",
            ...     assigned_user_id=1,
            ... )
            >>> print(f"Created lead with ID: {new_id}")

        Note:
            The API does not validate data. Ensure you provide valid field values.
        """
        data = {"crmid": 0, **fields}
        result = self._http.post(self._edit_endpoint, data=data)

        if isinstance(result, int):
            return result
        if isinstance(result, str) and result.isdigit():
            return int(result)
        if isinstance(result, dict) and "record_id" in result:
            return int(result["record_id"])
        return 0

    def update(self, crmid: int, **fields: Any) -> int:
        """
        Update an existing record.

        Args:
            crmid: The CRM ID of the record to update.
            **fields: Field values to update. Only provided fields are changed;
                other fields retain their current values.

        Returns:
            The CRM ID of the updated record.

        Example:
            >>> client.contacts.update(
            ...     crmid=12345,
            ...     email="newemail@example.com",
            ...     phone="555-1234",
            ... )
        """
        data = {"crmid": crmid, **fields}
        result = self._http.post(self._edit_endpoint, data=data)

        if isinstance(result, int):
            return result
        if isinstance(result, str) and result.isdigit():
            return int(result)
        return crmid

    def iterate(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
        batch_size: int = 100,
    ) -> Iterator[dict[str, Any]]:
        """
        Iterate over all records with automatic pagination.

        Yields records one at a time, automatically fetching new batches as needed.
        This is memory-efficient for large result sets.

        Args:
            query: Filter criteria. Can be a QueryBuilder instance or raw query string.
            keywords: Full-text search keywords.
            batch_size: Number of records to fetch per API call. Defaults to 100.

        Yields:
            Record dictionaries one at a time.

        Example:
            >>> for lead in client.leads.iterate():
            ...     print(lead["firstname"], lead["lastname"])
            >>> # With filtering
            >>> for contact in client.contacts.iterate(
            ...     query=query().equals("mailingcountry", "UK")
            ... ):
            ...     process_uk_contact(contact)
        """
        offset = 0
        while True:
            batch = self.list(
                query=query,
                keywords=keywords,
                limit_start=offset,
                limit_end=offset + batch_size,
            )
            if not batch:
                break
            yield from batch
            if len(batch) < batch_size:
                break
            offset += batch_size
