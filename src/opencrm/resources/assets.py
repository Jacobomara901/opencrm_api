from opencrm.models.asset import Asset
from opencrm.resources.base import BaseResource


class AssetsResource(BaseResource[Asset]):
    _module_name = "Assets"
    _list_endpoint = "get_asset_list"
    _list_full_endpoint = "get_asset_list_full"
    _count_endpoint = "get_asset_list_count"
    _get_endpoint = "get_asset"
    _edit_endpoint = "edit_asset"
    _model_class = Asset
