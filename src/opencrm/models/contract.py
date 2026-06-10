from decimal import Decimal

from pydantic import Field

from opencrm.models.base import CRMRecord


class Contract(CRMRecord):
    contact_id: int | None = Field(default=None, description="Contact ID")
    salesorder_id: int | None = Field(default=None, description="Sales Order ID")

    contracttype: str | None = Field(default=None, description="Type")

    cost_net: Decimal | None = Field(default=None, description="Costs (Exc VAT)")
    cost_gross: Decimal | None = Field(default=None, description="Costs (Inc VAT)")

    contracts_tags: str | None = Field(default=None)
