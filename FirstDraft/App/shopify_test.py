import shopify

from Config.config import settings

shopify_access_token = settings.SHOPIFY_ACCESS_TOKEN
shopify_store = settings.SHOPIFY_STORE
shopify_api_key = settings.SHOPIFY_API_KEY
shopify_password = settings.SHOPIFY_PASSWORD
api_version = settings.SHOPIFY_API_VERSION
shop_url = f"{shopify_store}.myshopify.com"

session = shopify.Session(
    shop_url=shop_url, version="2023-01", token=shopify_access_token
)
shopify.ShopifyResource.activate_session(session)

orders = shopify.Order.find()
# for order in orders:
#     print(type(order))
# order


shopify.ShopifyResource.clear_session()
