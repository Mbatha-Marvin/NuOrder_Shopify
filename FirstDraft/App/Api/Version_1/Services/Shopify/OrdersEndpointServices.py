import httpx, requests
from loguru import logger
from enum import Enum
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

    def getHeaders(self, header: str):
        if header.upper() == "GET" or header.upper() == "DELETE":
            return {
                "X-Shopify-Access-Token": self.shopify_access_token,
            }
        elif header.upper() == "POST" or header.upper() == "PUT":
            return {
                "X-Shopify-Access-Token": self.shopify_access_token,
                "Content-Type": "application/json",
            }
        else:
            raise Exception("Invalid HTTP Method")

    def makeRequest(self, method: str, url: str, data: dict = None):
        headers = self.getHeaders(header="GET")
        response = httpx.request(
            method=method.upper(), url=url, headers=headers, data=data, timeout=None
        )
        logger.info(f"{response.status_code = }")

        return response

    def getListOfOrders(
        self,
        status: str = str(ShopifyOrderStatus.ANY.value),
    ):
        url = f"https://{self.shopify_store}.myshopify.com/admin/api/{self.api_version}/orders.json?status={status}"
        # headers = self.getHeaders(header="GET")
        # response = httpx.get(url=url, headers=headers)
        # logger.info(f"{response.status_code = }")

        return self.makeRequest(method="GET", url=url)

    def getOrderByID(self, order_id: int):
        url = f"https://{self.shopify_store}.myshopify.com/admin/api/{self.api_version}/orders/{order_id}.json?fields=id%2Cline_items%2Cname%2Ctotal_price"
        # headers = self.getHeaders(header="GET")
        # response = httpx.get(url=url, headers=headers)
        # logger.info(f"{response.status_code = }")
        return self.makeRequest(method="GET", url=url)

    def getOrderCount(
        self,
        status: str = str(ShopifyOrderStatus.ANY.value),
    ):
        url = f"https://{self.shopify_store}.myshopify.com/admin/api/{self.api_version}/orders/count.json?status={status}"
        # headers = self.getHeaders(header="GET")
        # response = httpx.get(url=url, headers=headers)
        # logger.info(f"{response.status_code = }")
        return self.makeRequest(method="GET", url=url)

    def getProductByID(self):
        url = f"https://{self.shopify_store}.myshopify.com/admin/api/{self.api_version}/products.json"
        # headers = self.getHeaders(header="GET")
        # response = httpx.get(url=url, headers=headers)
        # logger.info(f"{response.status_code = }")
        return self.makeRequest(method="GET", url=url)

    def getProductCount(self):
        url = f"https://{self.shopify_store}.myshopify.com/admin/api/{self.api_version}/products/count.json"
        # headers = self.getHeaders(header="GET")
        # response = httpx.get(url=url, headers=headers)
        # logger.info(f"{response.status_code = }")
        return self.makeRequest(method="GET", url=url)
