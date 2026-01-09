from typing import TYPE_CHECKING, Any, Generic, TypeVar

from opencrm.models.base import CRMRecord, PaginationParams
from opencrm.utils.query import QueryBuilder

if TYPE_CHECKING:
    from opencrm.client import HTTPClient

T = TypeVar("T", bound=CRMRecord)


class BaseResource(Generic[T]):
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
        response = self._http.get(self._get_endpoint, data={"crmid": crmid})
        if isinstance(response, dict):
            return response
        return {}

    def create(self, **fields: Any) -> int:
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
    ):
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
