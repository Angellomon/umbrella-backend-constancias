from fastapi import FastAPI
from loguru import logger

from .core.config import get_settings
from .core.logging import setup_loguru
from .api.v1.api import router as api_router


s = get_settings()

app = FastAPI(openapi_url=f"{s.BASE_URL}/openapi.json")

app.add_event_handler("startup", setup_loguru)

logger.debug(s.BASE_URL)

app.include_router(api_router, prefix=s.BASE_URL)
