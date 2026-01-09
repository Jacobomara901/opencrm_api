from opencrm.models.company import Company
from opencrm.resources.base import BaseResource


class CompaniesResource(BaseResource[Company]):
    _module_name = "Companies"
    _list_endpoint = "get_company_list"
    _count_endpoint = "get_company_list_count"
    _get_endpoint = "get_company"
    _edit_endpoint = "edit_company"
    _model_class = Company
