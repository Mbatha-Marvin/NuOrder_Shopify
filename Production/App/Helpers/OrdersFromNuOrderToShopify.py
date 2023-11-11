import json
from typing import List
from pathlib import Path

from loguru import logger
from Shopify.EndpointServices import shopify_order_services
from Helpers.Models import (
    BillingAdress,
    ExistingCustomer,
    LineItem,
    NewCustomer,
    Order,
    BaseOrder,
    ShippingAddress,
)


class NuOrderToShopify:
    def __init__(self, nuorder_order: dict) -> None:
        self.nuorder_order = nuorder_order
        logger.info(f'{self.nuorder_order["_id"] = }')

    def createBaseOrder(self) -> BaseOrder:
        line_items = self.getLineItems()
        if self.nuorder_order.get("retailer").get("buyer_email") == "":
            email = "johndoe@nuorder.com"
        else:
            email = self.nuorder_order.get("retailer").get("buyer_email")
        name = f"N-{self.nuorder_order.get('_id')}"

        if self.nuorder_order.get("order_tags"):
            tags_list: list = self.nuorder_order.get("order_tags")
            tags = ", ".join(tags_list)
        else:
            tags = None

        processed_at = self.nuorder_order.get("modified_on")
        source_identifier = f'N-{self.nuorder_order.get("_id")}'
        total_price: str = str(self.nuorder_order.get("total"))
        confirmation_number = f'N-{self.nuorder_order.get("order_number")}'

        if self.nuorder_order.get("customer_po_number"):
            po_number = self.nuorder_order.get("customer_po_number")
        else:
            po_number = None

        total_discounts: str = str(
            self.nuorder_order.get("order_discounts").get("total_applied")
        )
        if float(total_discounts) < 0:
            total_discounts = "0.00"
        subtotal_price: str = str(
            self.nuorder_order.get("order_discounts").get("discounted_total")
        )
        if float(subtotal_price) < 0:
            total_discounts = "0.00"

        return BaseOrder(
            confirmation_number=confirmation_number,
            line_items=line_items,
            email=email,
            name=name,
            tags=tags,
            # presentment_currency=presentment_currency,
            processed_at=processed_at,
            source_identifier=source_identifier,
            total_price=total_price,
            po_number=po_number,
            total_discounts=total_discounts,
            subtotal_price=subtotal_price,
        )

    def createCustomerOrder(self) -> dict:
        nuorder_customer_email = self.nuorder_order.get("retailer").get("buyer_email")

        shopify_customer_emails = shopify_order_services.getCustomerEmails()
        base_order = self.createBaseOrder()

        if nuorder_customer_email in shopify_customer_emails:
            shopify_customer_id = (
                json.loads(
                    shopify_order_services.getCustomerDetailsByEmail(
                        nuorder_customer_email
                    ).content
                )
                .get("customers")[0]
                .get("id")
            )

            customer = ExistingCustomer(id=shopify_customer_id)
            order = {
                **base_order.model_dump(exclude_none=True),
                **customer.model_dump(exclude_none=True),
            }

            return {"order": order}
        else:
            name = self.nuorder_order.get("retailer").get("buyer_name").split(" ", 1)
            if len(name) == 2:
                first_name = name[0]
                last_name = name[1]
            elif len(name) == 1 and name[0]:
                first_name = name[0]
                last_name = "N-last_name"
            else:
                first_name = "N-first_name"
                last_name = "N-last_name"

            if self.nuorder_order.get("retailer").get("buyer_email") == "":
                customer_email = "johndoe@nuorder.com"
            else:
                customer_email = self.nuorder_order.get("retailer").get("buyer_email")
            customer = NewCustomer(
                first_name=first_name, last_name=last_name, email=customer_email
            )
            billing_address = self.getBillingAddress()
            shipping_address = self.getShippingAddress()

            if billing_address:
                order = {
                    "billing_address": {
                        **billing_address.model_dump(exclude_none=True)
                    },
                    "shipping_address": {
                        **shipping_address.model_dump(exclude_none=True)
                    },
                    "customer": {**customer.model_dump(exclude_none=True)},
                    **base_order.model_dump(exclude_none=True),
                }
            else:
                order = {
                    "customer": {**customer.model_dump(exclude_none=True)},
                    **base_order.model_dump(exclude_none=True),
                }

            return {"order": order}

    def loadFromJsonFile(self, relative_path: str):
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent
        file_path = BASE_DIR / f"{relative_path}"
        with open(file=file_path) as json_file:
            data = json.load(json_file)
        return data

    def getLineItems(self) -> List[LineItem]:
        logger.info("Generating Shopify Line Items")
        nuorder_line_items: List[dict] = self.nuorder_order["line_items"]
        shopify_line_items = []
        for item in nuorder_line_items:
            title: str = f'N-{item.get("product").get("style_number")}'
            price: str = str(item.get("sizes", "0.00")[0].get("price", "0.00"))
            if float(price) < 0:
                price = "0.00"
            quantity: int = self.nuorder_order.get("total_quantity", 0)
            if quantity < 0:
                quantity = 0
            item_id: str = item.get("product").get("_id")
            sku: str = item.get("product").get("style_number")
            name: str = f"N-{item_id}"

            shopify_line_items.append(
                LineItem(
                    title=title,
                    price=price,
                    quantity=quantity,
                    id=item_id,
                    sku=sku,
                    name=name,
                )
            )

            # logger.info(f"{len(shopify_line_items) = }")

        logger.success("Shopify Line Items Created")
        logger.info(f"{len(shopify_line_items) = }")
        return shopify_line_items

    def getBillingAddress(self) -> BillingAdress:
        if self.nuorder_order.get("billing_address", None):
            name = self.nuorder_order.get("retailer").get("buyer_name").split(" ", 1)
            if len(name) == 2:
                first_name = name[0]
                last_name = name[1]
            elif len(name) == 1 and name[0]:
                first_name = name[0]
                last_name = "N-last_name"
            else:
                first_name = "N-first_name"
                last_name = "N-last_name"
            address1 = self.nuorder_order.get("billing_address").get("line_1")
            zipcode = self.nuorder_order.get("billing_address").get("zip")
            city = self.nuorder_order.get("billing_address").get("city")
            country = self.nuorder_order.get("billing_address").get("country")

            logger.success("Shopify Shipping Address Generated")

            return ShippingAddress(
                first_name=first_name,
                last_name=last_name,
                address1=address1,
                city=city,
                province=city,
                country=country,
                zip=zipcode,
            )
        else:
            return None

    def getShippingAddress(self) -> ShippingAddress | None:
        if self.nuorder_order.get("billing_address", None):
            name = self.nuorder_order.get("retailer").get("buyer_name").split(" ", 1)
            if len(name) == 2:
                first_name = name[0]
                last_name = name[1]
            elif len(name) == 1 and name[0]:
                first_name = name[0]
                last_name = "N-last_name"
            else:
                first_name = "N-first_name"
                last_name = "N-last_name"
            address1 = self.nuorder_order.get("billing_address").get("line_1")
            zipcode = self.nuorder_order.get("billing_address").get("zip")
            city = self.nuorder_order.get("billing_address").get("city")
            country = self.nuorder_order.get("billing_address").get("country")

            logger.success("Shopify Shipping Address Generated")

            return ShippingAddress(
                first_name=first_name,
                last_name=last_name,
                address1=address1,
                city=city,
                province=city,
                country=country,
                zip=zipcode,
            )
        else:
            return None
