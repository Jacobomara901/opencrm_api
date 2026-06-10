from pydantic import Field

from opencrm.models.base import CRMRecord


class User(CRMRecord):
    user_name: str | None = Field(default=None, description="Username")
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email1: str | None = Field(default=None, description="Email")
    status: str | None = Field(default=None, description="Active / Inactive")

    @property
    def display_name(self) -> str:
        name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        if name:
            return name
        return self.user_name or self.email1 or ""
