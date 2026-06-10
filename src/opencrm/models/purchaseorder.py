from datetime import date
from decimal import Decimal

from pydantic import Field

from opencrm.models.base import CRMRecord


class PurchaseOrder(CRMRecord):
    subject: str | None = Field(default=None)
    purchaseorder_no: str | None = Field(default=None, description="Order Number")
    postatus: str | None = Field(default=None, description="Status")

    vendor_id: int | None = Field(default=None, description="Vendor / Supplier ID")
    contact_id: int | None = Field(default=None, description="Contact ID")
    requisition_no: str | None = Field(default=None, description="Requisition Number")
    tracking_no: str | None = Field(default=None, description="Tracking Number")

    duedate: date | None = Field(default=None, description="Due Date")
    issue_date: date | None = Field(default=None, description="Issue Date")

    subtotal: Decimal | None = Field(default=None, description="Sub Total")
    total: Decimal | None = Field(default=None, description="Grand Total")
    taxtype: str | None = Field(default=None, description="Tax Type")
    discount_percent: Decimal | None = Field(default=None, description="Discount %")
    discount_amount: Decimal | None = Field(default=None, description="Discount Amount")
    s_h_amount: Decimal | None = Field(default=None, description="Shipping & Handling")
    s_h_percent: Decimal | None = Field(default=None, description="S&H %")
    currency_id: int | None = Field(default=None, description="Currency ID")
    conversion_rate: Decimal | None = Field(default=None, description="Conversion Rate")

    bill_street: str | None = Field(default=None, description="Billing Address")
    bill_city: str | None = Field(default=None)
    bill_code: str | None = Field(default=None)
    bill_country: str | None = Field(default=None)
    ship_street: str | None = Field(default=None, description="Shipping Address")
    ship_city: str | None = Field(default=None)
    ship_code: str | None = Field(default=None)
    ship_country: str | None = Field(default=None)

    terms_conditions: str | None = Field(default=None, description="Terms & Conditions")
    purchaseorder_tags: str | None = Field(default=None)
