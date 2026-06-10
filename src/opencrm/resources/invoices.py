from opencrm.models.invoice import Invoice
from opencrm.resources.base import BaseResource


class InvoicesResource(BaseResource[Invoice]):
    _module_name = "Invoices"
    _list_endpoint = "get_invoice_list"
    _list_full_endpoint = "get_invoice_list_full"
    _count_endpoint = "get_invoice_list_count"
    _get_endpoint = "get_invoice"
    _edit_endpoint = "edit_invoice"
    _model_class = Invoice
