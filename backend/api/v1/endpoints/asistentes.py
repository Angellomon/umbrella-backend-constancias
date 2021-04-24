from fastapi import APIRouter, Depends, Query, Security, status
from fastapi.exceptions import HTTPException
from pydantic import EmailStr

from ....core.oauth import get_scopes
from ....crud.asistentes import crear_asistente as _crear_asistente
from ....crud.asistentes import get_asistente as _get_asistente
from ....crud.asistentes import get_asistentes as _get_asistentes
from ....crud.asistentes import update_asistente as _update_asistente
from ....crud.asistentes import remove_asistente as _remove_asistente
from ....models.asistentes import Asistente, AsistenteCreate, AsistenteUpdate
from ....models.users import User
from ..deps import Database, get_current_user, get_database

router = APIRouter(tags=["Asistentes"])
s = get_scopes()


@router.get("/", response_model=list[Asistente])
async def get_asistentes(
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.READ_ASISTENTES]),
):
    asistentes = await _get_asistentes(db)

    return asistentes


@router.get("/buscar", response_model=Asistente)
async def get_asistente(
    db: Database = Depends(get_database), correo: EmailStr = Query(...)
):
    asistente = await _get_asistente(db, correo)

    if asistente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"asistente no encontrado (correo={correo})",
        )

    return asistente


@router.post("/", response_model=Asistente)
async def crear_asistente(
    asistente_data: AsistenteCreate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.CREATE_ASISTENTES]),
):
    asistente = await _crear_asistente(db, asistente_data)

    return asistente


@router.patch("/{folio}", response_model=Asistente)
async def update_asistente(
    folio: str,
    asistente_data: AsistenteUpdate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.UPDATE_ASISTENTES]),
):
    asistente = await _update_asistente(db, folio, asistente_data)

    if asistente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"asistente no encontrado (folio={folio})",
        )

    return asistente


@router.delete("/{folio}", response_model=Asistente)
async def remove_asistente(
    folio: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    asistente = await _remove_asistente(db, folio)

    if asistente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"folio no encontrado (folio={folio})"
        )

    return asistente
