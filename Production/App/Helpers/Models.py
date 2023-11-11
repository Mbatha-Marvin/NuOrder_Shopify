from pydantic import BaseModel
from typing import List


class BillingAdress(BaseModel):
    first_name: str
    last_name: str
    address1: str
    # phone: str | None
    city: str
    province: str | None = None
    country: str
    zip: str


class ShippingAddress(BaseModel):
    first_name: str
    last_name: str
    address1: str
    # phone: str | None
    city: str
    province: str | None = None
    country: str
    zip: str


class NewCustomer(BaseModel):
    first_name: str
    last_name: str
    email: str


class ExistingCustomer(BaseModel):
    id: int


class LineItem(BaseModel):
    title: str
    price: str
    quantity: int
    # grams: str | None = None
    # tax_lines: List[dict] | None = None
    id: str | None = None
    sku: str | None = None
    name: str | None = None


class BaseOrder(BaseModel):
    billing_address: BillingAdress | None = None
    confirmation_number: str | None = None
    email: str
    # financial_status: str
    line_items: List[LineItem]
    name: str
    # presentment_currency: str
    processed_at: str
    shipping_address: ShippingAddress | None = None
    source_identifier: str
    tags: str | None = None
    total_price: str
    po_number: str | None = None
    total_discounts: str
    subtotal_price: str


class Order(BaseOrder):
    customer: NewCustomer | ExistingCustomer
