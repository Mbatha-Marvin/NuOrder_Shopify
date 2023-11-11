import httpx, json, requests
from enum import Enum
from typing import List
from loguru import logger
from Config.config import settings
from oauthlib.oauth1 import Client, SIGNATURE_HMAC_SHA1


class NuOrderOrderStatus(Enum):
    Draft = "draft"
    Review = "review"
    Pending = "pending"
    Approved = "approved"
    Processed = "processed"
    Shipped = "shipped"
    Cancelled = "cancelled"


class NuOrderOrdersServices:
    def __init__(
        self,
    ) -> None:
        self.application_name = settings.NUORDER_APPLICATION_NAME
        self.consumer_key = settings.NUORDER_CUSTOMER_KEY
        self.consumer_secret_key = settings.NUORDER_CUSTOMER_SECRET_KEY
        self.token = settings.NUORDER_TOKEN_KEY
        self.token_secret = settings.NUORDER_TOKEN_SERCRET
        self.base_url = settings.NUORDER_BASE_URL
        self.client = Client(
            client_key=self.consumer_key,
            client_secret=self.consumer_secret_key,
            resource_owner_key=self.token,
            resource_owner_secret=self.token_secret,
            signature_method=SIGNATURE_HMAC_SHA1,
        )

    def makeRequest(self, method: str, url: str, request_body: dict = None):
        uri, headers, body = self.client.sign(
            uri=url, http_method=method.upper(), body=request_body
        )
        response = httpx.request(
            method=method, url=uri, headers=headers, data=body, timeout=None
        )
        logger.info(f"{response.status_code = }")
        return response

    def makePostRequest(self, url: str, data: dict = None):
        data = json.dumps(data)
        options = {"Content-Type": "application/json"}
        uri, headers, body = self.client.sign(
            uri=url,
            http_method="POST",
            body=data,
        )
        response = httpx.request(
            method="POST", url=uri, headers=headers, data=body, timeout=None
        )
        logger.info(f"{response.status_code = }")
        return response

    def getOrdersByStatus(self, status: str):
        url = f"{self.base_url}/orders/{status}/detail?__populate=__payments"
        response = self.makeRequest("GET", url=url)
        return response

    def getOrdersIDListByStatus(self, status: str):
        url = f"{self.base_url}/orders/{status}/list"
        response = self.makeRequest("GET", url=url)
        return response

    def getOrderByID(self, order_id: str):
        url = f"{self.base_url}/order/{order_id}?__populate=__payments"
        response = self.makeRequest("GET", url=url)
        return response

    def getOrderByNumber(self, order_number: str):
        url = f"{self.base_url}/order/number/{order_number}?__populate=__payments"
        response = self.makeRequest("GET", url=url)
        return response

    def getProductByID(self, product_id: str):
        url = f"{self.base_url}/product/{product_id}"
        response = self.makeRequest("GET", url=url)
        return response

    def updateOrderStatusByID(self, status: str, order_id):
        url = f"{self.base_url}/order/{order_id}/{status}"
        response = self.makeRequest("POST", url=url)
        return response

    def updateOrder(self, order_id, updated_data):
        url = f"{self.base_url}/order/{order_id}"
        response = self.makePostRequest(url=url, data=updated_data)
        return response
    
    def patchOrderField(self, order_id, new_value, field):
        url = f"{self.base_url}/order/{order_id}/set/{field}/{new_value}"
        response = self.makeRequest("POST", url=url)
        return response
        pass


nuorder_order_services = NuOrderOrdersServices()
