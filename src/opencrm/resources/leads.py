from opencrm.models.lead import Lead
from opencrm.resources.base import BaseResource


class LeadsResource(BaseResource[Lead]):
    _module_name = "Leads"
    _list_endpoint = "get_lead_list"
    _count_endpoint = "get_lead_list_count"
    _get_endpoint = "get_lead"
    _edit_endpoint = "edit_lead"
    _model_class = Lead
