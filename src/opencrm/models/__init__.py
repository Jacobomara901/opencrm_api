from opencrm.models.base import CRMRecord, ListResponse, OpenCRMModel, PaginationParams
from opencrm.models.company import Company
from opencrm.models.contact import Contact
from opencrm.models.helpdesk import Helpdesk
from opencrm.models.lead import Lead
from opencrm.models.opportunity import Opportunity
from opencrm.models.project import Project

__all__ = [
    "OpenCRMModel",
    "CRMRecord",
    "ListResponse",
    "PaginationParams",
    "Lead",
    "Contact",
    "Company",
    "Project",
    "Helpdesk",
    "Opportunity",
]
