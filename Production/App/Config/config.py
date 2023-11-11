from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    NUORDER_APPLICATION_NAME: str
    NUORDER_BASE_URL: str 
    NUORDER_TEST_BASE_URL: str 
    NUORDER_TOKEN_KEY: str
    NUORDER_TOKEN_SERCRET: str 
    NUORDER_CUSTOMER_KEY: str 
    NUORDER_CUSTOMER_SECRET_KEY: str 
    DATABASE_URL: str 
    SHOPIFY_ACCESS_TOKEN: str 
    SHOPIFY_API_VERSION: str 
    SHOPIFY_API_KEY: str 
    SHOPIFY_PASSWORD: str
    SHOPIFY_STORE: str 
    
    APP_TITLE: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    APP_DEBUG: bool

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     app_name: str = "Awesome API"
#     admin_email: str
#     items_per_user: int = 50

#     model_config = SettingsConfigDict(env_file=".env")

