from opencrm.models.contract import Contract
from opencrm.resources.base import BaseResource


class ContractsResource(BaseResource[Contract]):
    _module_name = "Contracts"
    _list_endpoint = "get_contract_list"
    _list_full_endpoint = "get_contract_list_full"
    _count_endpoint = "get_contract_list_count"
    _get_endpoint = "get_contract"
    _edit_endpoint = "edit_contracts"
    _model_class = Contract
