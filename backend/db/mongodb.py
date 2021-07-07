from typing import Optional

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
)
from motor.core import AgnosticCollection

DBSession = Optional[AsyncIOMotorClientSession]


class Database:
    client: AsyncIOMotorClient

    constancias_db: AsyncIOMotorDatabase

    @property
    def asistentes_collection(self) -> AgnosticCollection:
        return self.constancias_db["asistentes"]

    @property
    def entidades_collection(self) -> AgnosticCollection:
        return self.constancias_db["entidades"]

    @property
    def users_collection(self) -> AgnosticCollection:
        return self.constancias_db["users"]

    @property
    def eventos(self) -> AgnosticCollection:
        return self.constancias_db["eventos"]


db = Database()


def get_database() -> Database:
    return db
