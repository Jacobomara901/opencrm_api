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
from opencrm.models.quote import Quote
from opencrm.models.purchaseorder import PurchaseOrder
from opencrm.models.salesorder import SalesOrder
from opencrm.resources.assets import AssetsResource
from opencrm.resources.contracts import ContractsResource
from opencrm.resources.purchaseorders import PurchaseOrdersResource
from opencrm.resources.quotes import QuotesResource
from opencrm.resources.salesorders import SalesOrdersResource


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


class TestQuotesResource:
    def test_endpoints(self):
        assert QuotesResource._list_endpoint == "get_quote_list"
        assert QuotesResource._list_full_endpoint == "get_quote_list_full"
        assert QuotesResource._count_endpoint == "get_quote_list_count"
        assert QuotesResource._get_endpoint == "get_quote"
        assert QuotesResource._edit_endpoint == "edit_quote"
        assert QuotesResource._model_class is Quote

    def test_client_property(self, client):
        assert isinstance(client.quotes, QuotesResource)

    def test_model_field_types(self):
        assert _annotated_type(Quote, "subject") == (str,)
        assert _annotated_type(Quote, "quotestage") == (str,)
        assert _annotated_type(Quote, "account_id") == (int,)
        assert _annotated_type(Quote, "validtill") == (date,)
        assert _annotated_type(Quote, "terms_conditions") == (str,)

    def test_model_inherits_crm_record(self):
        assert {"crmid", "assigned_user_id"} <= set(Quote.model_fields)


class TestSalesOrdersResource:
    def test_endpoints(self):
        assert SalesOrdersResource._list_endpoint == "get_salesorder_list"
        assert SalesOrdersResource._list_full_endpoint == "get_salesorder_list_full"
        assert SalesOrdersResource._count_endpoint == "get_salesorder_list_count"
        assert SalesOrdersResource._get_endpoint == "get_salesorder"
        assert SalesOrdersResource._edit_endpoint == "edit_salesorder"
        assert SalesOrdersResource._model_class is SalesOrder

    def test_client_property(self, client):
        assert isinstance(client.salesorders, SalesOrdersResource)

    def test_model_field_types(self):
        assert _annotated_type(SalesOrder, "subject") == (str,)
        assert _annotated_type(SalesOrder, "sostatus") == (str,)
        assert _annotated_type(SalesOrder, "quote_id") == (int,)
        assert _annotated_type(SalesOrder, "duedate") == (date,)
        assert _annotated_type(SalesOrder, "salesorder_tags") == (str,)

    def test_model_inherits_crm_record(self):
        assert {"crmid", "assigned_user_id"} <= set(SalesOrder.model_fields)


class TestPurchaseOrdersResource:
    def test_endpoints(self):
        assert PurchaseOrdersResource._list_endpoint == "get_purchaseorder_list"
        assert (
            PurchaseOrdersResource._list_full_endpoint == "get_purchaseorder_list_full"
        )
        assert PurchaseOrdersResource._count_endpoint == "get_purchaseorder_list_count"
        assert PurchaseOrdersResource._get_endpoint == "get_purchaseorder"
        assert PurchaseOrdersResource._edit_endpoint == "edit_purchaseorder"
        assert PurchaseOrdersResource._model_class is PurchaseOrder

    def test_client_property(self, client):
        assert isinstance(client.purchaseorders, PurchaseOrdersResource)

    def test_model_field_types(self):
        assert _annotated_type(PurchaseOrder, "subject") == (str,)
        assert _annotated_type(PurchaseOrder, "purchaseorder_no") == (str,)
        assert _annotated_type(PurchaseOrder, "vendor_id") == (int,)
        assert _annotated_type(PurchaseOrder, "duedate") == (date,)
        assert _annotated_type(PurchaseOrder, "total") == (Decimal,)

    def test_model_inherits_crm_record(self):
        assert {"crmid", "assigned_user_id"} <= set(PurchaseOrder.model_fields)
