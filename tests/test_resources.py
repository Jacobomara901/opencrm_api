"""Structural tests for resource/model wiring.

These tests verify the shape of the typed wrappers (endpoint constants,
model fields, client properties) without making any HTTP calls.
"""

from datetime import date
from decimal import Decimal
from typing import get_args, get_origin

import pytest

from opencrm import OpenCRMClient
from opencrm.models.asset import Asset
from opencrm.models.contract import Contract
from opencrm.resources.assets import AssetsResource
from opencrm.resources.contracts import ContractsResource


@pytest.fixture()
def client():
    c = OpenCRMClient(system_name="test", api_key="k", pass_key="p")
    yield c
    c.close()


def _annotated_type(model_cls: type, field: str) -> tuple:
    info = model_cls.model_fields[field]
    args = get_args(info.annotation)
    if not args:
        return (info.annotation,)
    return tuple(a for a in args if a is not type(None))


class TestAssetsResource:
    def test_endpoints(self):
        assert AssetsResource._list_endpoint == "get_asset_list"
        assert AssetsResource._list_full_endpoint == "get_asset_list_full"
        assert AssetsResource._count_endpoint == "get_asset_list_count"
        assert AssetsResource._get_endpoint == "get_asset"
        assert AssetsResource._edit_endpoint == "edit_asset"
        assert AssetsResource._model_class is Asset

    def test_client_property(self, client):
        assert isinstance(client.assets, AssetsResource)

    def test_model_field_types(self):
        assert _annotated_type(Asset, "account_id") == (int,)
        assert _annotated_type(Asset, "contact_id") == (int,)
        assert _annotated_type(Asset, "product_id") == (int,)

    def test_model_inherits_crm_record(self):
        assert {"crmid", "assigned_user_id"} <= set(Asset.model_fields)


class TestContractsResource:
    def test_endpoints(self):
        assert ContractsResource._list_endpoint == "get_contract_list"
        assert ContractsResource._list_full_endpoint == "get_contract_list_full"
        assert ContractsResource._count_endpoint == "get_contract_list_count"
        assert ContractsResource._get_endpoint == "get_contract"
        assert ContractsResource._edit_endpoint == "edit_contracts"
        assert ContractsResource._model_class is Contract

    def test_client_property(self, client):
        assert isinstance(client.contracts, ContractsResource)

    def test_model_field_types(self):
        assert _annotated_type(Contract, "contact_id") == (int,)
        assert _annotated_type(Contract, "salesorder_id") == (int,)
        assert _annotated_type(Contract, "contracttype") == (str,)
        assert _annotated_type(Contract, "cost_net") == (Decimal,)
        assert _annotated_type(Contract, "contracts_tags") == (str,)

    def test_model_inherits_crm_record(self):
        assert {"crmid", "assigned_user_id"} <= set(Contract.model_fields)
