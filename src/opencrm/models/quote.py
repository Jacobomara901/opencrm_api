from datetime import date

from pydantic import Field

from opencrm.models.base import CRMRecord


class Quote(CRMRecord):
    subject: str | None = Field(default=None)
    quotestage: str | None = Field(default=None, description="Quote Stage")
    quotetype: str | None = Field(default=None, description="Type")

    account_id: int | None = Field(default=None, description="Company ID")
    contact_id: int | None = Field(default=None, description="Contact ID")
    potential_id: int | None = Field(default=None, description="Opportunity ID")

    validtill: date | None = Field(default=None, description="Valid Till")

    bill_street: str | None = Field(default=None, description="Billing Address")
    bill_city: str | None = Field(default=None)
    bill_code: str | None = Field(default=None)
    bill_country: str | None = Field(default=None)
    ship_street: str | None = Field(default=None, description="Shipping Address")
    ship_city: str | None = Field(default=None)
    ship_code: str | None = Field(default=None)
    ship_country: str | None = Field(default=None)

    terms_conditions: str | None = Field(default=None, description="Terms & Conditions")
