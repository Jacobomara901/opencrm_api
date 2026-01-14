from opencrm.models.activity import Activity
from opencrm.resources.base import BaseResource


class ActivitiesResource(BaseResource[Activity]):
    _module_name = "Activities"
    _list_endpoint = "get_activity_list"
    _count_endpoint = "get_activity_list_count"
    _get_endpoint = "get_activity"
    _edit_endpoint = "edit_activity"
    _model_class = Activity
