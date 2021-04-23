from typing import Optional

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)

DBSession = Optional[AsyncIOMotorClientSession]


class Database:
    client: AsyncIOMotorClient

    naequina_db: AsyncIOMotorDatabase

    @property
    def asistentes_collection(self) -> AsyncIOMotorDatabase:
        return self.naequina_db["asistentes"]

    @property
    def entidades_collection(self) -> AsyncIOMotorDatabase:
        return self.naequina_db["entidades"]


db = Database()


def get_database() -> Database:
    return db