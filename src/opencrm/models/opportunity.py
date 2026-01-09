from datetime import date
from decimal import Decimal

from pydantic import Field

from opencrm.models.base import CRMRecord


class Opportunity(CRMRecord):
    potentialname: str | None = Field(default=None, description="Opportunity Name")
    potentialtype: str | None = Field(default=None, description="Type")
    sales_stage: str | None = Field(default=None, description="Sales Stage")
    leadsource: str | None = Field(default=None, description="Lead Source")
    nextstep: str | None = Field(default=None, description="Next Step")

    accountid: int | None = Field(default=None, description="Company ID")
    contactid: int | None = Field(default=None, description="Contact ID")
    campaignid: int | None = Field(default=None, description="Campaign ID")
    projectid: int | None = Field(default=None, description="Project ID")
    single_event_id: int | None = Field(default=None, description="Event ID")
    parent_id: int | None = Field(default=None, description="Related To ID")
    email: str | None = Field(default=None)

    amount: Decimal | None = Field(default=None)
    previous_amount: Decimal | None = Field(default=None)
    gain_loss: Decimal | None = Field(default=None)
    weightedamount: Decimal | None = Field(default=None, description="Weighted Amount")
    probability: int | None = Field(default=None, description="Probability %")
    salescommission: Decimal | None = Field(default=None, description="Sales Commission")

    start_date: date | None = Field(default=None, description="Start Date")
    closingdate: date | None = Field(default=None, description="Expected Close Date")
    activedays: int | None = Field(default=None, description="Active Period (days)")

    commission_approved: bool | None = Field(default=None)
    commission_approved_date: date | None = Field(default=None)

    def_currency: str | None = Field(default=None, description="Currency")
    cost_centre: str | None = Field(default=None)
    vat_rate: int | None = Field(default=None, description="VAT Rate %")

    potential_tags: str | None = Field(default=None)
    actionplan_id: int | None = Field(default=None, description="Action Plan ID")
    emailplan: int | None = Field(default=None, description="Email Plan ID")
    reassigned_date: date | None = Field(default=None)
