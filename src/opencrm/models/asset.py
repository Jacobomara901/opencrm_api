from pydantic import Field

from opencrm.models.base import CRMRecord


class Asset(CRMRecord):
    account_id: int | None = Field(default=None, description="Company ID")
    contact_id: int | None = Field(default=None, description="Contact ID")
    product_id: int | None = Field(default=None, description="Product ID")
