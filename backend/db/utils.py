from fastapi import Depends
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from ..core.config import Settings, get_settings
from .mongodb import Database, get_database


async def connect(settings: Settings = Depends(get_settings)):
    settings = get_settings()

    logger.info("conectándose a la base de datos...")

    db = get_database()
    db.client = AsyncIOMotorClient(
        str(settings.MONGODB_URL),
        uuidRepresentation="standard",
    )

    db.cnaequina_db = db.client["CNAEQUINA"]

    logger.info("conexión exitosa a la base de datos :D")


async def disconnect(db: Database = Depends(get_database)):
    db.client.close()
