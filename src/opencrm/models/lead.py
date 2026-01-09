from datetime import date
from typing import Optional

from pydantic import Field

from opencrm.models.base import CRMRecord


class Lead(CRMRecord):
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    company: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    mobile: str | None = Field(default=None)
    fax: str | None = Field(default=None)
    homephone: str | None = Field(default=None)

    designation: str | None = Field(default=None, description="Job Title")
    leadsource: str | None = Field(default=None)
    leadstatus: str | None = Field(default=None)
    leadtype: str | None = Field(default=None)
    industry: str | None = Field(default=None)
    rating: str | None = Field(default=None)
    annualrevenue: str | None = Field(default=None)
    noofemployees: str | None = Field(default=None)

    lane: str | None = Field(default=None, description="Street")
    lane2: str | None = Field(default=None, description="Street 2")
    city: str | None = Field(default=None)
    state: str | None = Field(default=None, description="County")
    code: str | None = Field(default=None, description="Postal Code")
    country: str | None = Field(default=None)

    website: str | None = Field(default=None)
    greeting: str | None = Field(default=None)
    dob: date | None = Field(default=None, description="Date of Birth")

    do_not_email: bool | None = Field(default=None)
    do_not_phone: bool | None = Field(default=None, alias="tps")
    do_not_fax: bool | None = Field(default=None, alias="fps")
    do_not_livechat: bool | None = Field(default=None, alias="donotlivechat")

    consent_to_processing: bool | None = Field(default=None)
    data_processing_consent_given: bool | None = Field(default=None)
    date_consent_given: date | None = Field(default=None)
    consent_given_to: str | None = Field(default=None)
    righttobeforgotten: bool | None = Field(default=None)
    righttobeforgotten_date: date | None = Field(default=None)

    portal: str | None = Field(default=None, description="Portal User")
    login: str | None = Field(default=None, description="Username")
    password: str | None = Field(default=None, description="Password")
    portal_islocked: bool | None = Field(default=None)

    subscription: str | None = Field(default=None, description="Comma-separated subscriptions")
    leaddetails_tags: str | None = Field(default=None, description="Comma-separated tags")
