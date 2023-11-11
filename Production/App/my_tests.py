import json, datetime
from pathlib import Path
from loguru import logger
from pprint import pprint
from Config.config import settings
from Helpers.OrdersFromNuOrderToShopify import NuOrderToShopify
from NuOrder.EndpointServices import NuOrderOrdersServices, NuOrderOrderStatus
from Shopify.EndpointServices import ShopifyAdminOrderServices, ShopifyOrderStatus


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


################ - NuOrder Tests And Fetch Data - ###########################
nuorder_order_services = NuOrderOrdersServices()
nuorder_order_status = str(NuOrderOrderStatus.Processed.value)

################ - Shopify Tests And Fetch Data - ###########################

shopify_order_services = ShopifyAdminOrderServices()
test_order_id = "4930083487786"
test_order: dict = json.loads(
    shopify_order_services.getOrderByID(order_id=test_order_id).content
).get("order", None)

test_email_1 = "info@townducktest1.com"
test_email_1 = "info@townducktest2.com"

if test_order:
    test_order.update({"email": test_email_1})


print(json.dumps(test_order))
