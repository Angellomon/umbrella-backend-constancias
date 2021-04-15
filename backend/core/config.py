import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "/api/v1"
    SECRET_KEY: str = "aninspiringcompany"
    PROJECT_NAME: str
    # SECRET_KEY: str = secrets.token_urlsafe(32)

    class Config:
        env_file = ".env" if os.environ.get("MODE") == "PROD" else ".env.local"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
