from opencrm.models.quote import Quote
from opencrm.resources.base import BaseResource


class QuotesResource(BaseResource[Quote]):
    _module_name = "Quotes"
    _list_endpoint = "get_quote_list"
    _list_full_endpoint = "get_quote_list_full"
    _count_endpoint = "get_quote_list_count"
    _get_endpoint = "get_quote"
    _edit_endpoint = "edit_quote"
    _model_class = Quote
