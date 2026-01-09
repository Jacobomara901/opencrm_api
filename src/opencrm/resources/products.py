from opencrm.models.product import Product
from opencrm.resources.base import BaseResource


class ProductsResource(BaseResource[Product]):
    """
    Resource for managing OpenCRM Product records.

    Example:
        >>> products = client.products.list()
        >>> product = client.products.get(crmid=123)
        >>> new_id = client.products.create(
        ...     productname="Widget",
        ...     productcode="WDG-001",
        ...     unit_price=29.99,
        ...     assigned_user_id=1,
        ... )
    """

    _module_name = "Products"
    _list_endpoint = "get_product_list"
    _count_endpoint = "get_product_list_count"
    _get_endpoint = "get_product"
    _edit_endpoint = "edit_product"
    _model_class = Product
