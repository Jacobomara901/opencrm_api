from opencrm.models.contact import Contact
from opencrm.resources.base import BaseResource


class ContactsResource(BaseResource[Contact]):
    _module_name = "Contacts"
    _list_endpoint = "get_contact_list"
    _count_endpoint = "get_contact_list_count"
    _get_endpoint = "get_contact"
    _edit_endpoint = "edit_contact"
    _model_class = Contact
