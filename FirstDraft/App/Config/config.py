from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    NUORDER_APPLICATION_NAME: str = Field(default="", env="NUORDER_APPLICATION_NAME")
    NUORDER_BASE_URL: str = Field(default="", env="NUORDER_BASE_URL")
    NUORDER_TEST_BASE_URL: str = Field(default="", env="NUORDER_TEST_BASE_URL")
    NUORDER_TOKEN_KEY: str = Field(default="", env="NUORDER_TOKEN_KEY")
    NUORDER_TOKEN_SERCRET: str = Field(default="", env="NUORDER_TOKEN_SERCRET")
    NUORDER_CUSTOMER_KEY: str = Field(default="", env="NUORDER_CUSTOMER_KEY")
    NUORDER_CUSTOMER_SECRET_KEY: str = Field(
        default="", env="NUORDER_CUSTOMER_SECRET_KEY"
    )
    DATABASE_URL: str = Field(default="", env="DATABASE_URL")
    SHOPIFY_ACCESS_TOKEN: str = Field(default="", env="SHOPIFY_ACCESS_TOKEN")
    SHOPIFY_API_VERSION: str = Field(default="", env="SHOPIFY_API_VERSION")
    SHOPIFY_API_KEY: str = Field(default="", env="SHOPIFY_API_KEY")
    SHOPIFY_PASSWORD: str = Field(default="", env="SHOPIFY_PASSWORD")
    SHOPIFY_STORE: str = Field(default="", env="SHOPIFY_STORE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
