import os
from functools import lru_cache

from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    BASE_URL: str = "/api/v1"
    SECRET_KEY: str = "aninspiringcompany"
    PROJECT_NAME: str
    STATIC_DIR: str = "backend/static"
    TEMPLATES_DIR: str = "backend/templates"
    TEST_TEMPLATE: str = "test-pdf.html"

    MONGODB_URL: AnyUrl
    # SECRET_KEY: str = secrets.token_urlsafe(32)

    class Config:
        env_file = ".env" if os.environ.get("MODE") == "PROD" else ".env.local"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()