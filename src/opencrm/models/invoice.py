from datetime import date

from pydantic import Field

from opencrm.models.base import CRMRecord


class Invoice(CRMRecord):
    subject: str | None = Field(default=None)
    invoicestatus: str | None = Field(default=None, description="Status")
    customerno: str | None = Field(default=None, description="Customer Number")

    account_id: int | None = Field(default=None, description="Company ID")
    contact_id: int | None = Field(default=None, description="Contact ID")
    salesorder_id: int | None = Field(default=None, description="Sales Order ID")
    potential_id: int | None = Field(default=None, description="Opportunity ID")

    invoicedate: date | None = Field(default=None, description="Invoice Date")
    duedate: date | None = Field(default=None, description="Due Date")
    paiddate: date | None = Field(default=None, description="Paid Date")

    bill_street: str | None = Field(default=None, description="Billing Address")
    bill_city: str | None = Field(default=None)
    bill_code: str | None = Field(default=None)
    bill_country: str | None = Field(default=None)
    ship_street: str | None = Field(default=None, description="Shipping Address")
    ship_city: str | None = Field(default=None)
    ship_code: str | None = Field(default=None)
    ship_country: str | None = Field(default=None)

    terms_conditions: str | None = Field(default=None, description="Terms & Conditions")
    invoice_tags: str | None = Field(default=None)
