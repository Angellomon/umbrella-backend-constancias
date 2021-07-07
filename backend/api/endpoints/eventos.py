from fastapi.param_functions import Security
from backend.models.users import User
from typing import List, Optional

from fastapi import APIRouter, Depends

from ...core.errors import EventoNotFound
from ...crud.eventos import crear_evento as _crear_evento
from ...crud.eventos import delete_evento as _delete_evento
from ...crud.eventos import get_evento as _get_evento
from ...crud.eventos import get_eventos as _get_eventos
from ...crud.eventos import update_evento as _update_evento
from ...models.eventos import Evento, EventoCreate, EventoUpdate
from ..deps import Database, get_current_user, get_database

router = APIRouter(tags=["Eventos"])


@router.post("/", response_model=Evento)
async def crear_evento(
    evento_data: EventoCreate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    evento = await _crear_evento(db, evento_data)

    return evento


@router.get("/", response_model=List[Evento])
async def get_eventos(
    clave_empresa: Optional[str] = None,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    eventos = await _get_eventos(db, clave_empresa=clave_empresa)

    return eventos


@router.get("/{clave_evento}", response_model=Evento)
async def get_evento(
    clave_evento: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    evento = await _get_evento(db, clave_evento)

    if evento is None:
        raise EventoNotFound(clave_evento)

    return evento


@router.patch("/{clave_evento}", response_model=Evento)
async def update_evento(
    clave_evento: str,
    evento_data: EventoUpdate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    evento = await _update_evento(db, clave_evento, evento_data)

    if evento is None:
        raise EventoNotFound(clave_evento)

    return evento


@router.delete("/{clave_evento}", response_model=Evento)
async def delete_evento(
    clave_evento: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    evento = await _delete_evento(db, clave_evento)

    if evento is None:
        raise EventoNotFound(clave_evento)

    return evento
