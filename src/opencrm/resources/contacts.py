from typing import Any

from opencrm.models.contact import Contact
from opencrm.resources.base import BaseResource, _parse_edit_result


class ContactsResource(BaseResource[Contact]):
    _module_name = "Contacts"
    _list_endpoint = "get_contact_list"
    _list_full_endpoint = "get_contact_list_full"
    _count_endpoint = "get_contact_list_count"
    _get_endpoint = "get_contact"
    _edit_endpoint = "edit_contact"
    _model_class = Contact

    def update_custom1(self, crmid: int, **fields: Any) -> int:
        """Update a contact via the secondary edit_contact_custom1 endpoint."""
        return self._edit_via("edit_contact_custom1", crmid, fields)

    def update_custom2(self, crmid: int, **fields: Any) -> int:
        """Update a contact via the secondary edit_contact_custom2 endpoint."""
        return self._edit_via("edit_contact_custom2", crmid, fields)

    def _edit_via(self, endpoint: str, crmid: int, fields: dict[str, Any]) -> int:
        data = {"crmid": crmid, **fields}
        result = self._http.post(endpoint, data=data)
        return _parse_edit_result(result, fallback=crmid)
