from opencrm.models.salesorder import SalesOrder
from opencrm.resources.base import BaseResource


class SalesOrdersResource(BaseResource[SalesOrder]):
    _module_name = "SalesOrders"
    _list_endpoint = "get_salesorder_list"
    _list_full_endpoint = "get_salesorder_list_full"
    _count_endpoint = "get_salesorder_list_count"
    _get_endpoint = "get_salesorder"
    _edit_endpoint = "edit_salesorder"
    _model_class = SalesOrder
