from typing import Optional
from ..db.mongodb import Database, DBSession
from ..models.counters import Entidades, EntityCounter


async def get_count(
    db: Database, /, entity: Entidades, *, session: DBSession = None
) -> Optional[EntityCounter]:
    collection = db.entidades_collection

    from loguru import logger

    logger.debug({"clave": f"{entity}"})

    entity_doc = await collection.find_one({"clave": f"{entity}"}, session=session)

    return EntityCounter(**entity_doc) if entity_doc else None


async def increment_count(
    db: Database, /, entity: Entidades, *, session: DBSession = None
) -> Optional[EntityCounter]:
    collection = db.entidades_collection

    entity_doc = await collection.find_one_and_update(
        {"clave": f"{entity}"}, {"$inc": {"valor": 1}}, session=session
    )

    return EntityCounter(**entity_doc) if entity_doc else None


async def set_count(
    db: Database, /, entity: Entidades, *, count: int = 0, session: DBSession = None
):
    collection = db.entidades_collection

    entity_doc = await collection.find_one_and_update(
        {"clave": f"{entity}"}, {"$set": {"valor": count}}, session=session
    )

    return EntityCounter(**entity_doc) if entity_doc else None


class EntityManager:
    entity: Entidades
    db: Database

    def __init__(self, entity: Entidades, db: Database):
        self.entity = entity
        self.db = db

    async def __aenter__(self) -> EntityCounter:
        entity = await get_count(self.db, self.entity)

        assert entity is not None, f"entidad no encontrada (entidad={self.entity}"

        entity.valor += 1

        return entity

    async def __aexit__(self, *args):
        await increment_count(self.db, self.entity)
