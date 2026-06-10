from opencrm.models.user import User
from opencrm.resources.base import BaseResource


class UsersResource(BaseResource[User]):
    _module_name = "Users"
    _list_endpoint = "get_user_list"
    _list_full_endpoint = "get_user_list_full"
    _count_endpoint = "get_user_list_count"
    _get_endpoint = "get_user_details"
    _model_class = User
