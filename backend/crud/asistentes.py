from typing import Optional
from backend.models.counters import Entidades
from ..models.asistentes import Asistente, AsistenteCreate, AsistenteUpdate
from ..crud.counters import EntityManager
from ..db.mongodb import Database, DBSession

from pymongo import ReturnDocument


async def crear_asistente(
    db: Database, /, asistente_data: AsistenteCreate, *, session: DBSession = None
) -> Asistente:
    collection = db.asistentes_collection

    async with EntityManager(Entidades.asistentes, db) as entity:
        folio = f"{entity.valor}".zfill(4)

        asistente = Asistente(**asistente_data.dict(), folio=folio)

        await collection.insert_one(asistente.dict(), session=session)

    return asistente


async def get_asistente(
    db: Database, /, correo: str, *, session: DBSession = None
) -> Optional[Asistente]:
    collection = db.asistentes_collection

    asistente = await collection.find_one({"correo": correo}, session=session)

    return Asistente(**asistente) if asistente else None


async def get_asistentes(db: Database, *, session: DBSession = None) -> list[Asistente]:
    collection = db.asistentes_collection

    cursor = collection.find({}, session=session)

    result = []

    async for doc in cursor:
        result.append(Asistente(**doc))

    return result


async def update_asistente(
    db: Database,
    /,
    folio: str,
    asistente_data: AsistenteUpdate,
    *,
    session: DBSession = None,
):
    collection = db.asistentes_collection

    asistente_doc = await collection.find_one_and_update(
        {"folio": folio},
        {"$set": asistente_data.dict(exclude_none=True)},
        return_document=ReturnDocument.AFTER,
        session=session,
    )

    return Asistente(**asistente_doc) if asistente_doc else None
