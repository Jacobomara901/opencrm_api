from opencrm.models.project import Project
from opencrm.resources.base import BaseResource


class ProjectsResource(BaseResource[Project]):
    _module_name = "Projects"
    _list_endpoint = "get_project_list"
    _count_endpoint = "get_project_list_count"
    _get_endpoint = "get_project"
    _edit_endpoint = "edit_project"
    _model_class = Project
