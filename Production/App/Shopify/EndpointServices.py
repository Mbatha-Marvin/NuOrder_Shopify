import json, httpx
from enum import Enum
from pathlib import Path
from loguru import logger
from pprint import pprint
from Config.config import settings


class ShopifyOrderStatus(Enum):
    ANY = "any"
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class ShopifyAdminOrderServices:
    def __init__(
        self,
    ) -> None:
        self.shopify_access_token = settings.SHOPIFY_ACCESS_TOKEN
        self.shopify_store = settings.SHOPIFY_STORE
        self.shopify_api_key = settings.SHOPIFY_API_KEY
        self.shopify_password = settings.SHOPIFY_PASSWORD
        self.api_version = settings.SHOPIFY_API_VERSION
        self.base_api_url = (
            f"https://{self.shopify_store}.myshopify.com/admin/api/{self.api_version}"
        )

    def getHeaders(self, method: str):
        if method == "GET" or method == "DELETE":
            return {
                "X-Shopify-Access-Token": self.shopify_access_token,
            }
        elif method == "POST" or method == "PUT":
            return {
                "X-Shopify-Access-Token": self.shopify_access_token,
                "Content-Type": "application/json",
            }
        else:
            raise Exception("Invalid HTTP Method")

    def makeRequest(self, method: str, url: str, data: dict | None = None):
        headers = self.getHeaders(method=method)
        if data:
            data = json.dumps(data)

        response = httpx.request(
            method=method, url=url, headers=headers, data=data, timeout=None
        )
        if response.status_code == 200:
            logger.success(f"{response.status_code =}")
        else:
            logger.warning(f"{response.status_code = }")

        return response

    def getListOfOrders(
        self,
        status: str = str(ShopifyOrderStatus.ANY.value),
    ):
        url = f"{self.base_api_url}/orders.json?status={status}"
        return self.makeRequest(method="GET", url=url)

    def getOrderByID(self, order_id: int):
        url = f"{self.base_api_url}/orders/{order_id}.json"
        return self.makeRequest(method="GET", url=url)

    def getOrderCount(
        self,
        status: str = str(ShopifyOrderStatus.ANY.value),
    ):
        url = f"{self.base_api_url}/orders/count.json?status={status}"
        return self.makeRequest(method="GET", url=url)

    def getProductByID(self, product_id: str):
        url = f"{self.base_api_url}/products/{product_id}.json"
        return self.makeRequest(method="GET", url=url)

    def getProductCount(self):
        url = f"{self.base_api_url}/products/count.json"
        return self.makeRequest(method="GET", url=url)

    def getListOfProducts(self):
        url = f"{self.base_api_url}/products.json"
        return self.makeRequest(method="GET", url=url)

    def createOrder(self, order_data: dict):
        url = f"{self.base_api_url}/orders.json"
        return self.makeRequest(method="POST", url=url, data=order_data)

    def saveToJsonFile(self, relative_path: str, json_data: dict):
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent
        file_path = BASE_DIR / f"{relative_path}"
        with open(file=file_path, mode="w") as outfile:
            json.dump(json_data, outfile, indent=2)
            logger.success(f"{file_path = } saved")

    def loadFromJsonFile(self, relative_path: str):
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent
        file_path = BASE_DIR / f"{relative_path}"
        with open(file=file_path) as json_file:
            data = json.load(json_file)
        return data

    def getCustomerIds(self) -> list:
        customers: dict = json.loads(self.getCustomers().content)
        customer_ids = []
        for customer in customers.get("customers"):
            customer_ids.append(customer.get("id"))
        return customer_ids

    def createWebhook(self, topic: str, address: str):
        url = f"{self.base_api_url}/webhooks.json"
        data = {
            "webhook": {
                "topic": f"{topic}",
                "address": f"{address}",
                "format": "json",
            }
        }
        
        return self.makeRequest(method="POST", url=url, data=data)
        
        pass

    def getCustomerEmails(self) -> list:
        customers: dict = json.loads(self.getCustomers().content)
        customer_emails = []
        for customer in customers.get("customers"):
            customer_emails.append(customer.get("email"))
        return customer_emails

    def getCustomerCount(self):
        url = f"{self.base_api_url}/customers/count.json"
        return self.makeRequest(method="GET", url=url)

    def getCustomerDetailsByID(self, customer_id: int):
        url = f"{self.base_api_url}/customers/{customer_id}.json"
        return self.makeRequest(method="GET", url=url)

    def getCustomerDetailsByEmail(self, customer_email: int):
        url = f"{self.base_api_url}/customers/search.json?query=email:{customer_email}"
        return self.makeRequest(method="GET", url=url)

    def getCustomers(self):
        url = f"{self.base_api_url}/customers.json"
        return self.makeRequest(method="GET", url=url)

    # def createBaseOrder(self, order_data: dict):
    #     url = f"{self.base_api_url}/orders.json"
    #     return self.makeRequest(method="POST", url=url, data=order_data)

    # def generateSkuProductIDMapping(self) -> dict:
    #     logger.info("Generating Shopify Product_ID:SKU HashMap ")
    #     sku_mapper = "Helpers/sku_to_product_id_mappings.json"
    #     sku_to_product = {}
    #     response = self.getListOfProducts()
    #     if response.status_code == 200:
    #         product_list: dict = json.loads(response.content).get("products", None)
    #         if product_list:
    #             for product in product_list:
    #                 variants = product["variants"]

    #                 for variant in variants:
    #                     sku_to_product.update(
    #                         {
    #                             f"{variant['sku']}": {
    #                                 "product_id": variant["product_id"],
    #                                 "product_title": product["title"],
    #                                 "vendor": product["vendor"],
    #                                 "product_type": product["product_type"],
    #                                 "variant_id": variant["id"],
    #                                 "variant_title": variant["title"],
    #                                 "price": variant["price"],
    #                                 "fulfillment_service": variant[
    #                                     "fulfillment_service"
    #                                 ],
    #                                 "taxable": variant["taxable"],
    #                                 "grams": variant["grams"],
    #                                 "requires_shipping": variant["requires_shipping"],
    #                             }
    #                         }
    #                     )

    #         self.saveToJsonFile(
    #             relative_path=sku_mapper,
    #             json_data=sku_to_product,
    #         )
    #         logger.info(f"{len(list(sku_to_product.keys()))} sku(s) values found")
    #         return sku_to_product

    #     else:
    #         logger.error(f"{response.text = }")

    # def loadSkuProductIDMapping(self):
    #     return self.loadFromJsonFile("Helpers/sku_to_product_id_mappings.json")


shopify_order_services = ShopifyAdminOrderServices()
