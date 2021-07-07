from typing import Optional

from pymongo import ReturnDocument

from ..crud.eventos import get_evento, update_evento
from ..db.mongodb import Database, DBSession
from ..models.asistentes import (
    Asistente,
    AsistenteCreate,
    AsistentesAlta,
    AsistenteUpdate,
)
from ..models.eventos import EventoUpdate


async def buscar_asistente(
    db: Database, /, correo: str, clave_evento: str
) -> Optional[Asistente]:
    asistente_doc = await db.asistentes.find_one(
        {"correo": correo, "clave_evento": clave_evento}
    )

    return Asistente(**asistente_doc) if asistente_doc else None


async def crear_asistente(
    db: Database, /, asistente_data: AsistenteCreate, *, session: DBSession = None
) -> Asistente:
    evento = await get_evento(db, asistente_data.clave_evento)

    assert (
        evento is not None
    ), f"evento no encontrado (clave={asistente_data.clave_evento})"
    assert (
        await buscar_asistente(db, asistente_data.correo, evento.clave) is None
    ), f"el asistente ya se encuentra registrado en el evento (correo={asistente_data.correo}, evento={evento.nombre})"

    folio = evento.siguiente_folio

    asistente = Asistente(**asistente_data.dict(), folio=folio)

    await db.asistentes.insert_one(asistente.dict(), session=session)
    await update_evento(
        db, evento.clave, EventoUpdate(total_asistentes=evento.total_asistentes)
    )

    return asistente


async def crear_asistentes(
    db: Database,
    /,
    clave_evento: str,
    alta_data: AsistentesAlta,
    *,
    session: DBSession = None,
) -> list[Asistente]:
    await db.asistentes.delete_many({"clave_evento": clave_evento}, session=session)

    evento = await get_evento(db, clave_evento)

    assert evento is not None, f"evento no encontrado (clave={clave_evento})"

    evento.total_asistentes = 0
    evento.inicio_folio = alta_data.cuenta_inicial

    data = []

    for asistente in alta_data.asistentes:
        asistente.clave_evento = clave_evento
        data.append(Asistente(folio=evento.siguiente_folio, **asistente.dict()))

    await db.asistentes.insert_many([a.dict() for a in data])
    await update_evento(
        db, clave_evento, EventoUpdate(total_asistentes=evento.total_asistentes)
    )

    return data


async def get_asistente(
    db: Database, /, clave_asistente: str, *, session: DBSession = None
) -> Optional[Asistente]:
    asistente = await db.asistentes.find_one(
        {"clave": clave_asistente}, session=session
    )

    return Asistente(**asistente) if asistente else None


async def get_asistentes(db: Database, *, session: DBSession = None) -> list[Asistente]:
    cursor = db.asistentes.find({}, session=session)

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
    asistente_doc = await db.asistentes.find_one_and_update(
        {"folio": folio},
        {"$set": asistente_data.dict(exclude_none=True)},
        return_document=ReturnDocument.AFTER,
        session=session,
    )

    return Asistente(**asistente_doc) if asistente_doc else None


async def remove_asistente(db: Database, /, folio: str, *, session: DBSession = None):
    asistente_doc = await db.asistentes.find_one_and_delete(
        {"folio": folio}, session=session
    )

    return Asistente(**asistente_doc) if asistente_doc else None
