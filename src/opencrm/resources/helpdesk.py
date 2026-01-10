from opencrm.models.helpdesk import Helpdesk
from opencrm.resources.base import BaseResource


class HelpdeskResource(BaseResource[Helpdesk]):
    _module_name = "Helpdesk"
    _list_endpoint = "get_ticket_list"
    _count_endpoint = "get_ticket_list_count"
    _get_endpoint = "get_ticket"
    _edit_endpoint = "edit_ticket"
    _model_class = Helpdesk
