from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class OpenCRMModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="allow",
    )

    record_id: int | None = Field(default=None, alias="record_id")
    record_module: str | None = Field(default=None, alias="record_module")

    def to_api_dict(self) -> dict[str, Any]:
        data = self.model_dump(by_alias=True, exclude_none=True)
        result: dict[str, Any] = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                result[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, date):
                result[key] = value.strftime("%Y-%m-%d")
            elif isinstance(value, bool):
                result[key] = "1" if value else "0"
            else:
                result[key] = value
        return result


class CRMRecord(OpenCRMModel):
    crmid: int | None = Field(default=None)
    assigned_user_id: int | None = Field(default=None, alias="smownerid")
    permission: int | None = Field(default=None)
    description: str | None = Field(default=None)


class ListResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    items: list[dict[str, Any]] = Field(default_factory=list)
    total_count: int | None = None


class PaginationParams(BaseModel):
    limit_start: int | None = None
    limit_end: int | None = None
    keywords: str | None = None
    query_string: str | None = None
