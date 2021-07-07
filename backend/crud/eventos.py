from typing import List, Optional

from pymongo import ReturnDocument

from ..db.mongodb import Database
from ..models.eventos import Evento, EventoCreate, EventoUpdate


async def buscar_evento(db: Database, nombre: Optional[str]) -> Optional[Evento]:
    query = {}

    if query is not None:
        query["nombre"] = nombre

    evento_doc = await db.eventos.find_one(query)

    return Evento(**evento_doc) if evento_doc else None


async def crear_evento(db: Database, /, evento_data: EventoCreate) -> Evento:

    assert (
        await buscar_evento(db, evento_data.nombre) is None
    ), f"el evento ya existe ({evento_data.nombre})"

    evento = Evento(**evento_data.dict())

    await db.eventos.insert_one(evento.dict())

    return evento


async def get_eventos(db: Database) -> List[Evento]:
    cursor = db.eventos.find()

    eventos = []

    async for doc in cursor:
        eventos.append(Evento(**doc))

    return eventos


async def get_evento(db: Database, /, clave_evento: str) -> Optional[Evento]:
    evento_doc = await db.eventos.find_one({"clave": clave_evento})

    return Evento(**evento_doc) if evento_doc else None


async def update_evento(
    db: Database, /, clave_evento: str, evento_data: EventoUpdate
) -> Optional[Evento]:
    evento_doc = await db.eventos.find_one_and_update(
        {"clave": clave_evento},
        {"$set": evento_data.dict(exclude_none=True)},
        return_document=ReturnDocument.AFTER,
    )

    return Evento(**evento_doc) if evento_doc else None


async def delete_evento(db: Database, /, clave_evento: str) -> Optional[Evento]:
    evento_doc = await db.eventos.find_one_and_delete({"clave": clave_evento})

    return Evento(**evento_doc) if evento_doc else None
