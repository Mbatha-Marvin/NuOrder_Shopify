from Api.Version_1.Services.NuOrder.OrdersEndpointServices import (
    NuOrderOrdersServices,
    NuOrderOrderStatus,
)
from Api.Version_1.Services.Shopify.OrdersEndpointServices import (
    ShopifyAdminOrderServices,
    ShopifyOrderStatus,
)
from pprint import pprint
from Config.config import settings
import json


# Nu Order tests

nuorder_order_services = NuOrderOrdersServices()

nuorder_order_status = str(NuOrderOrderStatus.Processed.value)

# response: dict = nuorder_order_services.getOrdersByStatus(
#     status=nuorder_order_status
# ).json()
# pprint(response)

# order_id_list = nuorder_order_services.getOrdersIDListByStatus(
#     status=nuorder_order_status
# ).json()
# pprint(order_id_list, indent=2)

# test_order_id = "65089de8ce0aac042cc47b32"

# response = nuorder_order_services.getOrderByID(test_order_id)
# # pprint(response.content)
# pprint(response.json())


# test_product_id = "64229ea416f63f19d7ca3ed0"

# response = nuorder_order_services.getProductByID(test_product_id)
# pprint(response.content)
# # pprint(response.json())
# with open("App/Data/NuOrderProduct.json", "w") as outfile:
#     json.dump(response.json(), outfile, indent=2)


############################ Shopify tests ###############################

shopify_order_services = ShopifyAdminOrderServices()

# response: dict = shopify_order_services.getListOfOrders()
# orders: dict = response.json()
# pprint(orders["orders"][0])

# # sample_order = orders["orders"]
# with open("App/Data/ShopifyOrders.json", "w") as outfile:
#     json.dump(response, outfile, indent=2)

# response = shopify_order_services.getOrderCount()
# pprint(response.content)

# response = shopify_order_services.getProductCount()
# pprint(response.json())
