from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .core.logging import setup_loguru
from .api.api import router as api_router
from .db.utils import connect, disconnect

s = get_settings()

app = FastAPI(openapi_url=f"{s.BASE_URL}/openapi.json")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
    if s.MODE == "DEV"
    else [str(origin) for origin in s.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# hmmm

app.mount("/static", StaticFiles(directory=s.STATIC_DIR), name="static")

app.add_event_handler("startup", setup_loguru)
app.add_event_handler("startup", connect)
app.add_event_handler("shutdown", disconnect)

app.include_router(api_router)
