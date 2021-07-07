# import os
from functools import lru_cache
from typing import List, Literal

from pydantic import BaseSettings, AnyUrl
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    BASE_URL: str = "/"
    SECRET_KEY: str = "aninspiringcompany"
    PROJECT_NAME: str
    STATIC_DIR: str = "backend/static"
    TEMPLATES_DIR: str = "backend/templates"
    TEST_TEMPLATE: str = "naequina.html"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 240
    SERVER_NAME: str = "Constancias UMBERLLA"
    SERVER_HOST: str = "localhost"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    NANOID_SIZE: int = 10
    NANOID_ALPHA: str = "abcdefghijklmnopqrstuvwxyz1234567890"

    MONGODB_URL: AnyUrl
    MODE: Literal["DEV", "PROD"] = "DEV"
    # SECRET_KEY: str = secrets.token_urlsafe(32)

    class Config:
        env_file = ".env"  # if os.environ.get("MODE") == "PROD" else ".env.local"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
