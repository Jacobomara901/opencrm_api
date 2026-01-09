from datetime import date
from decimal import Decimal

from pydantic import Field

from opencrm.models.base import CRMRecord


class Product(CRMRecord):
    """
    OpenCRM Product record.

    Products can be standalone items or linked to sales records (quotes, orders, invoices).
    """

    productname: str | None = Field(default=None, description="Product Name")
    productcode: str | None = Field(default=None, description="Product Code")
    productcategory: str | None = Field(default=None, description="Product Category")
    product_status: str | None = Field(default=None, description="Product Status")
    subproducttype: str | None = Field(default=None, description="Sub Product Type")
    discontinued: bool | None = Field(
        default=None, description="Product Active (0=active, 1=discontinued)"
    )

    product_description: str | None = Field(default=None, description="Description")
    mini_description: str | None = Field(default=None, description="Mini Description")

    unit_price: Decimal | None = Field(default=None, description="Sell Price")
    buy_price: Decimal | None = Field(default=None, description="Buy Price")
    commissionrate: int | None = Field(default=None, description="Commission Rate (%)")
    commission_band: str | None = Field(default=None, description="Commission Band")

    manufacturer: str | None = Field(default=None)
    vendor_id: int | None = Field(default=None, description="Supplier Company ID")
    vendor_part_no: str | None = Field(default=None, description="Supplier Part No")

    qtyinstock: int | None = Field(default=None, description="Qty. in Stock")
    qtyindemand: int | None = Field(default=None, description="Qty. in Demand")
    reorderlevel: str | None = Field(default=None, description="Reorder Level")
    qty_per_unit: int | None = Field(default=None, description="Qty/Unit")

    location_warehouse: str | None = Field(default=None, description="Warehouse")
    location_shelf: str | None = Field(default=None, description="Shelf")
    location_bin: str | None = Field(default=None, description="Bin")

    serialno: str | None = Field(default=None, description="Serial No")
    batch_number: str | None = Field(default=None, description="Batch Number")
    model_revision: str | None = Field(default=None, description="Model Revision")

    sales_start_date: date | None = Field(default=None, description="Sales Start Date")
    sales_end_date: date | None = Field(default=None, description="Sales End Date")
    start_date: date | None = Field(default=None, description="Support Start Date")
    expiry_date: date | None = Field(default=None, description="Support Expiry Date")
    datein: date | None = Field(default=None, description="Date In")
    despatchdate: date | None = Field(default=None, description="Despatch Date")
    price_check_date: date | None = Field(default=None, description="Price Check Date")

    contract_term: int | None = Field(default=None, description="Contract Term (months)")

    nominal_code: str | None = Field(default=None, description="Sales Nominal Code")
    purch_nom_code: str | None = Field(default=None, description="Purchase Nominal Code")
    purch_nom_desc: str | None = Field(default=None, description="Purchase Nominal Description")
    glacct: str | None = Field(default=None, description="Nominal Account")
    taxclass: str | None = Field(default=None, description="Tax Class")
    def_currency: str | None = Field(default=None, description="Default Currency")

    usageunit: int | None = Field(default=None, description="Usage Unit")
    size: str | None = Field(default=None)
    weight_stock: int | None = Field(default=None, description="Weight (Kg)")
    prod_supplytype: str | None = Field(default=None, description="Supply Type")
    bundle_product: str | None = Field(default=None, description="Bundle Product")

    website: str | None = Field(default=None)
    productsheet: str | None = Field(default=None, description="Product Sheet")

    parentprodid: int | None = Field(default=None, description="Parent Product ID")
    customerid: int | None = Field(default=None, description="End User Contact ID")
    installerid: int | None = Field(default=None, description="Installer Company ID")

    products_tags: str | None = Field(default=None, description="Tags (comma-separated)")
    reassigned_date: date | None = Field(default=None)
