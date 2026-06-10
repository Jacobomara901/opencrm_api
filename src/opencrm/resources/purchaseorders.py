from opencrm.models.purchaseorder import PurchaseOrder
from opencrm.resources.base import BaseResource


class PurchaseOrdersResource(BaseResource[PurchaseOrder]):
    _module_name = "PurchaseOrders"
    _list_endpoint = "get_purchaseorder_list"
    _list_full_endpoint = "get_purchaseorder_list_full"
    _count_endpoint = "get_purchaseorder_list_count"
    _get_endpoint = "get_purchaseorder"
    _edit_endpoint = "edit_purchaseorder"
    _model_class = PurchaseOrder
