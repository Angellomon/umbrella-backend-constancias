from functools import lru_cache

from fastapi.templating import Jinja2Templates
from ...db.mongodb import Database, get_database

from ...core.config import Settings, get_settings


@lru_cache
def get_templates() -> Jinja2Templates:
    return Jinja2Templates(directory=get_settings().TEMPLATES_DIR)


__all__ = ["Settings", "get_settings", "Database", "get_database"]
