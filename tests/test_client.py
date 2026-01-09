import pytest
from opencrm import OpenCRMClient, query
from opencrm.exceptions import ConfigurationError


class TestOpenCRMClient:
    def test_requires_system_name(self):
        with pytest.raises(ConfigurationError, match="system_name is required"):
            OpenCRMClient(system_name="", api_key="key", pass_key="pass")

    def test_requires_api_credentials(self):
        with pytest.raises(ConfigurationError, match="api_key and pass_key are required"):
            OpenCRMClient(system_name="test", api_key="", pass_key="pass")

        with pytest.raises(ConfigurationError, match="api_key and pass_key are required"):
            OpenCRMClient(system_name="test", api_key="key", pass_key="")

    def test_invalid_auth_method(self):
        with pytest.raises(ConfigurationError, match="Invalid auth_method"):
            OpenCRMClient(
                system_name="test",
                api_key="key",
                pass_key="pass",
                auth_method="invalid",  # type: ignore
            )

    def test_client_has_resource_properties(self):
        client = OpenCRMClient(
            system_name="test",
            api_key="key",
            pass_key="pass",
        )

        assert hasattr(client, "leads")
        assert hasattr(client, "contacts")
        assert hasattr(client, "companies")
        assert hasattr(client, "projects")
        assert hasattr(client, "helpdesk")
        assert hasattr(client, "opportunities")
        assert hasattr(client, "products")

        client.close()


class TestQueryBuilder:
    def test_equals(self):
        q = query().equals("lastname", "Smith")
        assert q.build() == "lastname|=|Smith"

    def test_like(self):
        q = query().like("email", "%@example.com")
        assert q.build() == "email|LIKE|%@example.com"

    def test_begins_with(self):
        q = query().begins_with("company", "Acme")
        assert q.build() == "company|BEGINS|Acme"

    def test_ends_with(self):
        q = query().ends_with("phone", "1234")
        assert q.build() == "phone|ENDS|1234"

    def test_contains(self):
        q = query().contains("description", "important")
        assert q.build() == "description|CONTAINS|important"

    def test_empty_query(self):
        q = query()
        assert q.build() is None

    def test_clear(self):
        q = query().equals("name", "test")
        q.clear()
        assert q.build() is None
