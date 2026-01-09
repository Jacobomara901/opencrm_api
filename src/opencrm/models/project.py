from datetime import date
from decimal import Decimal

from pydantic import Field

from opencrm.models.base import CRMRecord


class Project(CRMRecord):
    name: str | None = Field(default=None)
    projectnum: str | None = Field(default=None, description="Project Number")
    projecttype: str | None = Field(default=None, description="Project Type")
    projectstatus: str | None = Field(default=None, description="Status")
    projpriority: str | None = Field(default=None, description="Priority")

    accountid: int | None = Field(default=None, description="Company ID")
    contactid: int | None = Field(default=None, description="Contact ID")
    salesorder_id: int | None = Field(default=None, description="Sales Order ID")
    parent_id: int | None = Field(default=None, description="Related To ID")
    email: str | None = Field(default=None)

    startdate: date | None = Field(default=None, description="Start Date")
    enddate: date | None = Field(default=None, description="End Date")
    targetend: date | None = Field(default=None, description="Target End Date")

    budget: Decimal | None = Field(default=None)
    cost_net: Decimal | None = Field(default=None, description="Costs (Exc VAT)")
    cost_gross: Decimal | None = Field(default=None, description="Costs (Inc VAT)")
    vat_rate: str | None = Field(default=None, description="VAT Rate %")

    time_m: str | None = Field(default=None, description="Project Time (minutes)")
    time_taken_m: int | None = Field(default=None, description="Chargeable Time (minutes)")
    nc_time_m: int | None = Field(default=None, description="Non Chargeable Time (minutes)")
    sched_time_m: int | None = Field(default=None, description="Scheduled Time (minutes)")

    active: bool | None = Field(default=None)
    private: bool | None = Field(default=None)
    showonportal: bool | None = Field(default=None, description="Show On Portal")
    showdocsonportal: bool | None = Field(default=None, description="Show Documents On Portal")

    projects_tags: str | None = Field(default=None)
    actionplan_id: int | None = Field(default=None, description="Action Plan ID")
    emailplan: int | None = Field(default=None, description="Email Plan ID")
    reassigned_date: date | None = Field(default=None)
