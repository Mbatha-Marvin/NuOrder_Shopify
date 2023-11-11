import json
from typing import List
from fastapi import Response
from loguru import logger
from Shopify.EndpointServices import shopify_order_services
from Helpers.OrdersFromNuOrderToShopify import NuOrderToShopify
from NuOrder.EndpointServices import NuOrderOrderStatus, nuorder_order_services


def fetchApprovedOrdersFromNuOrder() -> List[dict]:
    nuorder_order_status = str(NuOrderOrderStatus.Approved.value)
    return json.loads(
        nuorder_order_services.getOrdersByStatus(status=nuorder_order_status).content
    )


def processApprovedOrders() -> List[dict]:
    approved_orders = fetchApprovedOrdersFromNuOrder()
    processed_orders = []
    for order in approved_orders:
        nuorder_order_id = order.get("_id")
        mapper = NuOrderToShopify(nuorder_order=order)
        # processed_orders.append(mapper.createCustomerOrder())

        response = shopify_order_services.createOrder(mapper.createCustomerOrder())
        processed_orders.append(json.loads(response.content))

        # update nuorder status
        nuorder_order_services.updateOrderStatusByID(
            status="processed", order_id=nuorder_order_id
        )

    return processed_orders


def updateNuorderOrderField(shopify_data: dict):
    source_identifier = shopify_data.get("source_identifier")

    if source_identifier:
        # print(order_to_update)
        shopify_financial_status = shopify_data.get("financial_status")
        if shopify_financial_status:
            logger.info(f"Updating Nu -Order to {shopify_financial_status} ")
            if shopify_financial_status == "pending":
                new_status = "pending"
            elif shopify_financial_status == "paid":
                new_status = "processed"
            elif shopify_financial_status == "voided":
                new_status = "cancelled"
            elif shopify_financial_status == "approved":
                new_status = "approved"
            else:
                new_status = "pending"

        response = nuorder_order_services.updateOrderStatusByID(
            status=new_status, order_id=source_identifier[2:]
        )
        logger.info(f"Order status {source_identifier[2:]} Updated")
        
        if response.status_code == 304:
            return Response(content="Order Not Updated", status_code=200)

        return Response(content="Order Updated successfully", status_code=200)

    else:
        return Response(content="Order cant be processed", status_code=400)


def patchOrderField(shopify_data: dict, nuorder_field=None):
    source_identifier = shopify_data.get("source_identifier")

    if source_identifier:
        # order_to_update = nuorder_order_services.getOrderByID(
        #     order_id=source_identifier[2:])
        new_value = shopify_data.get("note")
        if nuorder_field:
            field = nuorder_field
        else:
            field = "notes"
        response = nuorder_order_services.patchOrderField(
            order_id=source_identifier[2:], field=field, new_value=new_value
        )
        logger.info(f"Order {source_identifier[2:]} Updated")

        return json.loads(response.content)


# def updateNuOrderOrderStatus(order:dict):
# pass
