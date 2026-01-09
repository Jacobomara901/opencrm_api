from opencrm.models.opportunity import Opportunity
from opencrm.resources.base import BaseResource


class OpportunitiesResource(BaseResource[Opportunity]):
    _module_name = "Opportunities"
    _list_endpoint = "get_opportunity_list"
    _count_endpoint = "get_opportunity_list_count"
    _get_endpoint = "get_opportunity"
    _edit_endpoint = "edit_opportunity"
    _model_class = Opportunity
