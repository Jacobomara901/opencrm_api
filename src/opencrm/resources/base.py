"""
Base resource class for OpenCRM API modules.

All resource classes (LeadsResource, ContactsResource, etc.) inherit from BaseResource.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, Iterator, TypeVar

from opencrm.models.base import CRMRecord
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
    _list_full_endpoint: str = ""
    _count_endpoint: str = ""
    _get_endpoint: str = ""
    _edit_endpoint: str = ""
    _model_class: type[T]

    def __init__(self, http: "HTTPClient") -> None:
        self._http = http

    def _parse_list_response(self, response: Any) -> list[dict[str, Any]]:
        if isinstance(response, dict):
            items = [response]
        elif isinstance(response, list):
            items = response
        else:
            return []
        return [_normalize_id(item) for item in items]

    @staticmethod
    def _resolve_query(query: QueryBuilder | str | None) -> str | None:
        if query is None:
            return None
        if isinstance(query, QueryBuilder):
            return query.build()
        return query or None

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

        query_str = self._resolve_query(query)
        if query_str:
            data["query_string"] = query_str

        if keywords:
            data["keywords"] = keywords

        result = self._http.post(self._count_endpoint, data=data)
        return _coerce_int(result, fallback=0)

    def _list(
        self,
        endpoint: str,
        query: QueryBuilder | str | None,
        keywords: str | None,
        limit_start: int | None,
        limit_end: int | None,
    ) -> list[dict[str, Any]]:
        data: dict[str, Any] = {}

        query_str = self._resolve_query(query)
        if query_str:
            data["query_string"] = query_str

        if keywords:
            data["keywords"] = keywords
        if limit_start is not None:
            data["limit_start"] = limit_start
        if limit_end is not None:
            data["limit_end"] = limit_end

        response = self._http.post(endpoint, data=data)
        return self._parse_list_response(response)

    def list(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
        limit_start: int | None = None,
        limit_end: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        List records with optional filtering and pagination.

        Returns minimal field projections via the standard ``get_*_list`` endpoint.

        Example:
            >>> leads = client.leads.list(limit_start=0, limit_end=50)
            >>> new_leads = client.leads.list(query=query().equals("leadstatus", "New"))
        """
        return self._list(
            self._list_endpoint, query, keywords, limit_start, limit_end
        )

    def list_full(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
        limit_start: int | None = None,
        limit_end: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        List records returning the full field set via the ``_full`` endpoint.

        These endpoints return ``id`` instead of ``crmid``; the response is
        normalized so ``crmid`` is always populated.

        Raises:
            NotImplementedError: If the resource has no ``_list_full_endpoint``.
        """
        if not self._list_full_endpoint:
            raise NotImplementedError(
                f"{self._module_name}: _full list endpoint not configured"
            )
        return self._list(
            self._list_full_endpoint, query, keywords, limit_start, limit_end
        )

    def list_all(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
        batch_size: int = 200,
    ) -> list[dict[str, Any]]:
        """Fetch every matching record by paginating ``list`` until exhausted."""
        return list(self.iterate(query=query, keywords=keywords, batch_size=batch_size))

    def list_all_full(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
        batch_size: int = 200,
    ) -> list[dict[str, Any]]:
        """Fetch every matching record using the ``_full`` endpoint."""
        return list(
            self.iterate_full(query=query, keywords=keywords, batch_size=batch_size)
        )

    def get(self, crmid: int) -> dict[str, Any]:
        """
        Retrieve a single record by its CRM ID.

        Args:
            crmid: The unique OpenCRM record ID.

        Returns:
            Dictionary containing all record fields.

        Raises:
            NotFoundError: If the record doesn't exist.
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
                You should always include ``assigned_user_id`` to set the owner.

        Returns:
            The CRM ID of the newly created record.
        """
        data = {"crmid": 0, **fields}
        result = self._http.post(self._edit_endpoint, data=data)
        return _parse_edit_result(result, fallback=0)

    def update(self, crmid: int, **fields: Any) -> int:
        """
        Update an existing record.

        Args:
            crmid: The CRM ID of the record to update.
            **fields: Field values to update. Only provided fields are changed;
                other fields retain their current values.

        Returns:
            The CRM ID of the updated record.
        """
        data = {"crmid": crmid, **fields}
        result = self._http.post(self._edit_endpoint, data=data)
        return _parse_edit_result(result, fallback=crmid)

    def iterate(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
        batch_size: int = 100,
    ) -> Iterator[dict[str, Any]]:
        """
        Iterate over all records with automatic pagination.

        Memory-efficient for large result sets.

        Example:
            >>> for lead in client.leads.iterate():
            ...     print(lead["firstname"], lead["lastname"])
        """
        yield from _paginate(self.list, query, keywords, batch_size)

    def iterate_full(
        self,
        query: QueryBuilder | str | None = None,
        keywords: str | None = None,
        batch_size: int = 100,
    ) -> Iterator[dict[str, Any]]:
        """Iterate over all records using the ``_full`` endpoint."""
        if not self._list_full_endpoint:
            raise NotImplementedError(
                f"{self._module_name}: _full list endpoint not configured"
            )
        yield from _paginate(self.list_full, query, keywords, batch_size)


def _normalize_id(item: Any) -> Any:
    if not isinstance(item, dict):
        return item
    if "crmid" in item or "id" not in item:
        return item
    item["crmid"] = item["id"]
    return item


def _coerce_int(value: Any, fallback: int) -> int:
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        return fallback
    trimmed = value.strip().strip('"')
    return int(trimmed) if trimmed.isdigit() else fallback


def _parse_edit_result(result: Any, fallback: int) -> int:
    coerced = _coerce_int(result, fallback=-1)
    if coerced != -1:
        return coerced
    if not isinstance(result, dict):
        return fallback
    for key in ("crmid", "record_id", "id"):
        coerced = _coerce_int(result.get(key), fallback=-1)
        if coerced != -1:
            return coerced
    return fallback


def _paginate(
    fetch: Callable[..., list[dict[str, Any]]],
    query: QueryBuilder | str | None,
    keywords: str | None,
    batch_size: int,
) -> Iterator[dict[str, Any]]:
    offset = 0
    while True:
        batch = fetch(
            query=query,
            keywords=keywords,
            limit_start=offset,
            limit_end=offset + batch_size,
        )
        if not batch:
            return
        yield from batch
        if len(batch) < batch_size:
            return
        offset += batch_size
