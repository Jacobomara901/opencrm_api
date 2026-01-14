from datetime import date
from decimal import Decimal

from pydantic import Field

from opencrm.models.base import CRMRecord


class Activity(CRMRecord):
    subject: str | None = Field(default=None)
    status: str | None = Field(default=None, alias="taskstatus")
    priority: str | None = Field(default=None, alias="taskpriority")

    date_start: date | None = Field(default=None, description="Start Date & Time")
    due_date: date | None = Field(default=None, description="Due Date")
    duration_hours: int | None = Field(default=None, description="Duration (hours)")

    parent_id: int | None = Field(default=None, description="Related To ID")
    contact_id: int | None = Field(default=None, description="Contact ID")
    accountid: int | None = Field(default=None, description="Company ID")
    single_asset_id: int | None = Field(default=None, description="Asset ID")

    category: str | None = Field(default=None)
    tasklist: str | None = Field(default=None, description="Task List")

    chargetime: str | None = Field(default=None, description="Charge Time")
    cost_net: Decimal | None = Field(default=None, description="Costs (Exc VAT)")
    cost_gross: Decimal | None = Field(default=None, description="Costs (Inc VAT)")
    vat_rate: int | None = Field(default=None, description="VAT Rate %")

    livechat_convo_url: str | None = Field(default=None, description="Conversation URL")
    cf_faqrating: int | None = Field(default=None, description="FAQ Rating")

    sendnotification: bool | None = Field(default=None, description="Send Notification To Owner")
    sendnotificationcont: bool | None = Field(
        default=None, description="Send Notification To Contact"
    )
    reminder_time: bool | None = Field(default=None, description="Send Reminder To Owner")
    reminder_time_cont: bool | None = Field(default=None, description="Send Reminder To Contact")
    showonportal: bool | None = Field(default=None, description="Show On Portal")
