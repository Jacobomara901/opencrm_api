from datetime import date

from pydantic import Field

from opencrm.models.base import CRMRecord


class Contact(CRMRecord):
    firstname: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    accountid: int | None = Field(default=None, description="Company ID")
    title: str | None = Field(default=None, description="Job Title")
    department: str | None = Field(default=None)
    contacttype: str | None = Field(default=None)
    leadsource: str | None = Field(default=None)
    greeting: str | None = Field(default=None)
    birthday: date | None = Field(default=None, description="Birthdate")

    email: str | None = Field(default=None, description="Business Email")
    email2: str | None = Field(default=None, description="Private Email")
    phone: str | None = Field(default=None, description="Office Phone")
    mobile: str | None = Field(default=None)
    homephone: str | None = Field(default=None)
    otherphone: str | None = Field(default=None)
    fax: str | None = Field(default=None)
    assistant: str | None = Field(default=None)
    assistantphone: str | None = Field(default=None)
    assistant_email: str | None = Field(default=None)

    mailingstreet: str | None = Field(default=None)
    mailingstreet2: str | None = Field(default=None)
    mailingcity: str | None = Field(default=None)
    mailingstate: str | None = Field(default=None, description="Mailing County")
    mailingzip: str | None = Field(default=None, description="Mailing Postcode")
    mailingcountry: str | None = Field(default=None)

    otherstreet: str | None = Field(default=None)
    otherstreet2: str | None = Field(default=None)
    othercity: str | None = Field(default=None)
    otherstate: str | None = Field(default=None)
    otherzip: str | None = Field(default=None)
    othercountry: str | None = Field(default=None)

    addressinherit: bool | None = Field(default=None)
    reportsto: int | None = Field(default=None, description="Reports To Contact ID")
    folder: str | None = Field(default=None)

    do_not_email: bool | None = Field(default=None)
    do_not_phone: bool | None = Field(default=None, alias="tps")
    do_not_fax: bool | None = Field(default=None, alias="fps")
    donotlivechat: bool | None = Field(default=None)

    consent_to_processing: bool | None = Field(default=None)
    data_processing_consent_given: bool | None = Field(default=None)
    date_consent_given: date | None = Field(default=None)
    consent_given_to: str | None = Field(default=None)
    righttobeforgotten: bool | None = Field(default=None)
    righttobeforgotten_date: date | None = Field(default=None)

    portal: str | None = Field(default=None)
    login: str | None = Field(default=None)
    password: str | None = Field(default=None)
    portal_islocked: bool | None = Field(default=None)
    canesign: bool | None = Field(default=None)

    support_start_date: date | None = Field(default=None)
    support_end_date: date | None = Field(default=None)
    sage_ref: str | None = Field(default=None)
    includeinsync: str | None = Field(default=None)
    subscription: str | None = Field(default=None)
    contactdetails_tags: str | None = Field(default=None)
