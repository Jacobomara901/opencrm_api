from datetime import date
from decimal import Decimal

from pydantic import Field

from opencrm.models.base import CRMRecord


class Helpdesk(CRMRecord):
    title: str | None = Field(default=None)
    status: str | None = Field(default=None)
    priority: str | None = Field(default=None)
    severity: str | None = Field(default=None)
    category: str | None = Field(default=None)
    support_queue: str | None = Field(default=None, description="Queue")

    contactid: int | None = Field(default=None, description="Contact ID")
    parent_id: int | None = Field(default=None, description="Related To (Contact/Company) ID")
    extra_parent_id: int | None = Field(default=None, description="3rd Party ID")
    contractid: int | None = Field(default=None, description="Contract ID")
    projectid: int | None = Field(default=None, description="Project ID")
    product_id: int | None = Field(default=None, description="Product ID")
    single_asset_id: int | None = Field(default=None, description="Asset ID")

    solution: str | None = Field(default=None)
    tech_solution: str | None = Field(default=None, description="Technical Solution")

    closedon: date | None = Field(default=None, description="Close Date")
    closedby: str | None = Field(default=None, description="Closed By")
    openedby: str | None = Field(default=None, description="Opened By")

    cost_net: Decimal | None = Field(default=None, description="Costs (Exc VAT)")
    cost_gross: Decimal | None = Field(default=None, description="Costs (Inc VAT)")

    showonportal: bool | None = Field(default=None, description="Show On Portal")
    email_to: str | None = Field(
        default=None, description="Additional Recipients (comma-separated)"
    )
    sent_to_support_email: str | None = Field(default=None)

    troubletickets_tags: str | None = Field(default=None)
    actionplan_id: int | None = Field(default=None, description="Action Plan ID")
    emailplan: int | None = Field(default=None, description="Email Plan ID")
    reassigned_date: date | None = Field(default=None)
