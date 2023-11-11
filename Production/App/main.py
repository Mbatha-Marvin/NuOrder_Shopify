import json, datetime
from fastapi import Body, FastAPI, Response
from pathlib import Path
from loguru import logger
from pprint import pprint
from Config.config import settings
from Shopify.EndpointServices import ShopifyAdminOrderServices
from Helpers.OrdersFromNuOrderToShopify import NuOrderToShopify
from Services.Endpoints import (
    processApprovedOrders,
    patchOrderField,
    fetchApprovedOrdersFromNuOrder,
    updateNuorderOrderField,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="NuOrder To Shopify",
    version="0.1.0",
    debug=True,
)


@app.get("/", tags=["Status"])
def health_check() -> dict:
    return {
        "name": settings.APP_TITLE,
        "version": "0.1.0",
        # "description": settings.description,
    }


@app.get("/shopify_orders", tags=["Shopify"])
def generate_shopify_order():
    shopify_order_services = ShopifyAdminOrderServices()

    # return json.loads(shopify_order_services.getCustomerCount().content)
    test_orders = shopify_order_services.loadFromJsonFile(
        "Data/NuOrderProcessedOrders.json"
    )
    orders = []
    for index, order in enumerate(test_orders):
        if index <= 10:
            mapper = NuOrderToShopify(nuorder_order=order)
            orders.append(mapper.createCustomerOrder())
        else:
            break

    return orders


@app.get("/nuorder/orders/approved", tags=["NuOrder"])
def getApprovedOrders():
    return fetchApprovedOrdersFromNuOrder()


@app.get("/nuorder/process_approved")
def processApproved():
    return processApprovedOrders()


@app.post("/shopify/webhook_processing")
def processWebhook(payload: dict = Body()):
    response = updateNuorderOrderField(shopify_data=payload)
    return response
    # return Response(status_code=200)


@app.post("/nuorder/patch_field")
def processWebhook(payload: dict = Body()):
    response = patchOrderField(shopify_data=payload)
    return response
    # return Response(status_code=200)
