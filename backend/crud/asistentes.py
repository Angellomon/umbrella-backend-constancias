from typing import Optional
from backend.models.counters import Entidades
from ..models.asistentes import (
    Asistente,
    AsistenteCreate,
    AsistenteUpdate,
    AsistentesAlta,
)
from ..crud.counters import EntityManager, set_count
from ..db.mongodb import Database, DBSession

from pymongo import ReturnDocument


def _generar_folio(folio: int, length: int = 4) -> str:
    return f"{folio}".zfill(length)


async def crear_asistente(
    db: Database, /, asistente_data: AsistenteCreate, *, session: DBSession = None
) -> Asistente:
    collection = db.asistentes_collection

    async with EntityManager(Entidades.asistentes, db) as entity:
        folio = _generar_folio(entity.valor)

        asistente = Asistente(**asistente_data.dict(), folio=folio)

        await collection.insert_one(asistente.dict(), session=session)

    return asistente


async def crear_asistentes(
    db: Database,
    /,
    alta_data: AsistentesAlta,
    *,
    session: DBSession = None,
) -> list[Asistente]:
    collection = db.asistentes_collection

    await collection.delete_many({}, session=session)

    i = alta_data.cuenta_inicial
    data = []

    for asistente in alta_data.asistentes:
        data.append(Asistente(folio=_generar_folio(i), **asistente.dict()))
        i += 1

    await collection.insert_many([a.dict() for a in data])

    await set_count(db, Entidades.asistentes, count=i)

    return data


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


async def remove_asistente(db: Database, /, folio: str, *, session: DBSession = None):
    collection = db.asistentes_collection

    asistente_doc = await collection.find_one_and_delete(
        {"folio": folio}, session=session
    )

    return Asistente(**asistente_doc) if asistente_doc else None
