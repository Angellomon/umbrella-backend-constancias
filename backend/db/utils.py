from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger

from ..core.config import Settings, get_settings
from .mongodb import get_database


@logger.catch
async def connect(settings: Settings = Depends(get_settings)):
    settings = get_settings()

    db = get_database()
    db.client = AsyncIOMotorClient(
        str(settings.MONGODB_URL),
        uuidRepresentation="standard",
    )

    db.constancias_db = db.client["CONSTANCIAS"]


@logger.catch
async def disconnect():
    db = get_database()
    db.client.close()
