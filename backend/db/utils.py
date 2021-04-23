from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger

from ..core.config import Settings, get_settings
from .mongodb import Database, get_database


@logger.catch
async def connect(settings: Settings = Depends(get_settings)):
    settings = get_settings()

    db = get_database()
    db.client = AsyncIOMotorClient(
        str(settings.MONGODB_URL),
        uuidRepresentation="standard",
    )

    db.naequina_db = db.client["NAEQUINA"]


@logger.catch
async def disconnect():
    db = get_database()
    db.client.close()
