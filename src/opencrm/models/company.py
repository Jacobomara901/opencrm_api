from datetime import date
from decimal import Decimal

from pydantic import Field

from opencrm.models.base import CRMRecord


class Company(CRMRecord):
    accountname: str | None = Field(default=None, description="Company Name")
    account_type: str | None = Field(default=None, description="Type")
    industry: str | None = Field(default=None)
    ownership: str | None = Field(default=None, description="Legal Format")
    rating: str | None = Field(default=None)
    employees: str | None = Field(default=None)
    annualrevenue: str | None = Field(default=None)
    companynumber: str | None = Field(default=None)
    proprietor: str | None = Field(default=None, description="Proprietor/Senior Partner")
    parentid: int | None = Field(default=None, description="Parent Company ID")

    email1: str | None = Field(default=None, description="Email")
    email2: str | None = Field(default=None, description="Other Email")
    phone: str | None = Field(default=None)
    otherphone: str | None = Field(default=None)
    fax: str | None = Field(default=None)
    website: str | None = Field(default=None)

    street: str | None = Field(default=None, description="Billing Address")
    bill_street_2: str | None = Field(default=None, description="Billing Address 2")
    city: str | None = Field(default=None, description="Billing City")
    state: str | None = Field(default=None, description="Billing County")
    code: str | None = Field(default=None, description="Billing Postcode")
    country: str | None = Field(default=None, description="Billing Country")
    billemail: str | None = Field(default=None, description="Billing Email")

    ship_street: str | None = Field(default=None, description="Shipping Address")
    ship_street_2: str | None = Field(default=None)
    ship_city: str | None = Field(default=None)
    ship_state: str | None = Field(default=None)
    ship_code: str | None = Field(default=None)
    ship_country: str | None = Field(default=None)
    shipemail: str | None = Field(default=None)

    reg_street: str | None = Field(default=None, description="Registered Address")
    reg_street_2: str | None = Field(default=None)
    reg_city: str | None = Field(default=None)
    reg_state: str | None = Field(default=None)
    reg_code: str | None = Field(default=None)
    reg_country: str | None = Field(default=None)
    address_inherit: bool | None = Field(default=None)

    do_not_email: bool | None = Field(default=None)
    do_not_phone: bool | None = Field(default=None, alias="tps")
    do_not_fax: bool | None = Field(default=None, alias="fps")

    consent_to_processing: bool | None = Field(default=None)
    data_processing_consent_given: bool | None = Field(default=None)
    date_consent_given: date | None = Field(default=None)
    consent_given_to: str | None = Field(default=None)
    righttobeforgotten: bool | None = Field(default=None)
    righttobeforgotten_date: date | None = Field(default=None)

    sage_ref: str | None = Field(default=None)
    vatnumber: str | None = Field(default=None, description="VAT Number")
    vatexempt: bool | None = Field(default=None)
    def_currency: str | None = Field(default=None, description="Default Currency")
    pricebook: int | None = Field(default=None, description="Pricebook ID")
    language: str | None = Field(default=None)

    paymenttype: str | None = Field(default=None, description="Account Type (Credit Control)")
    credit_limit: Decimal | None = Field(default=None)
    credit_limit_days: int | None = Field(default=None, description="Balance Days")
    credit_status: str | None = Field(default=None)
    stockfund: bool | None = Field(default=None, description="Credit Fund")
    creditcheckon: date | None = Field(default=None)
    creditcheckby: str | None = Field(default=None)

    outstanding_balance: Decimal | None = Field(default=None, description="Total Balance")
    due_balance: Decimal | None = Field(default=None)
    overdue_balance: Decimal | None = Field(default=None)
    currentspend: Decimal | None = Field(default=None, description="Current Spend")
    year_to_date: Decimal | None = Field(default=None, description="Opportunity YTD")

    majoraccount: bool | None = Field(default=None, description="Major Account")
    includeinsync: bool | None = Field(default=None)
    subscription: str | None = Field(default=None)
    account_tags: str | None = Field(default=None)
