from fastapi import APIRouter, Depends, Query, status
from fastapi.exceptions import HTTPException
from pydantic import EmailStr

from ....models.asistentes import Asistente, AsistenteCreate, AsistenteUpdate
from ..deps import Database, get_database
from ....crud.asistentes import (
    get_asistentes as _get_asistentes,
    get_asistente as _get_asistente,
    crear_asistente as _crear_asistente,
    update_asistente as _update_asistente,
)

router = APIRouter(tags=["Asistentes"])


@router.get("/", response_model=list[Asistente])
async def get_asistentes(db: Database = Depends(get_database)):
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
    asistente_data: AsistenteCreate, db: Database = Depends(get_database)
):
    asistente = await _crear_asistente(db, asistente_data)

    return asistente


@router.patch("/{folio}", response_model=Asistente)
async def update_asistente(
    folio: str, asistente_data: AsistenteUpdate, db: Database = Depends(get_database)
):
    asistente = await _update_asistente(db, folio, asistente_data)

    if asistente is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"asistente no encontrado (folio={folio})",
        )

    return asistente
