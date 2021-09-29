from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.param_functions import Query, Security
from pydantic.networks import EmailStr
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates

from ...core.errors import AsistenteNotFound, EventoNotFound
from ...core.oauth import get_scopes
from ...crud.eventos import crear_evento as _crear_evento
from ...crud.eventos import delete_evento as _delete_evento
from ...crud.eventos import get_evento as _get_evento
from ...crud.eventos import get_eventos as _get_eventos
from ...crud.eventos import update_evento as _update_evento

from ...crud.asistentes import buscar_asistente, crear_asistente as _crear_asistente
from ...crud.asistentes import get_asistentes as _get_asistentes
from ...crud.asistentes import crear_asistentes as _crear_asistentes
from ...crud.asistentes import update_asistente as _update_asistente
from ...crud.asistentes import remove_asistente as _remove_asistente
from ...models.asistentes import (
    Asistente,
    AsistenteCreate,
    AsistenteUpdate,
    AsistentesAlta,
)
from ...models.eventos import Evento, EventoCreate, EventoUpdate
from ...models.users import User
from ..deps import Database, get_current_user, get_database, get_templates
from weasyprint import HTML

router = APIRouter(tags=["Eventos"])
s = get_scopes()


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


@router.get("/{clave_evento}/asistentes")
async def get_asistentes_evento(
    clave_evento: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.CREATE_ASISTENTES]),
):
    asistentes = await _get_asistentes(db, clave_evento=clave_evento)

    return asistentes


@router.post("/{clave_evento}/asistentes", response_model=Asistente)
async def crear_asistente(
    clave_evento: str,
    asistente_data: AsistenteCreate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.CREATE_ASISTENTES]),
):

    asistente_data.clave_evento = clave_evento
    asistente = await _crear_asistente(db, asistente_data)

    return asistente


@router.get("/{clave_evento}/asistentes", response_model=List[Asistente])
async def get_asistentes(
    clave_evento: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.CREATE_ASISTENTES]),
):
    asistentes = await _get_asistentes(db, clave_evento=clave_evento)

    return asistentes


@router.post("/{clave_evento}/asistentes/many", response_model=list[Asistente])
async def crear_asistentes(
    clave_evento: str,
    alta_data: AsistentesAlta,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.CREATE_ASISTENTES]),
):
    asistentes = await _crear_asistentes(db, clave_evento, alta_data)

    return asistentes


@router.patch("/{clave_evento}/asistentes/{clave_asistente}", response_model=Asistente)
async def update_asistente(
    clave_evento: str,
    clave_asistente: str,
    asistente_data: AsistenteUpdate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.UPDATE_ASISTENTES]),
):
    asistente = await _update_asistente(
        db, clave_asistente, asistente_data, clave_evento=clave_evento
    )

    if asistente is None:
        raise AsistenteNotFound(clave_asistente)

    return asistente


@router.delete("/{clave_evento}/asistentes/{clave_asistente}", response_model=Asistente)
async def remove_asistente(
    clave_asistente: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    asistente = await _remove_asistente(db, clave_asistente)

    if asistente is None:
        raise AsistenteNotFound(clave_asistente)

    return asistente


@router.get("/{clave_evento}/asistentes/buscar", response_model=Asistente)
async def get_asistente(
    clave_evento: str,
    request: Request,
    db: Database = Depends(get_database),
    correo: EmailStr = Query(...),
    templates: Jinja2Templates = Depends(get_templates),
):
    evento = await _get_evento(db, clave_evento)

    if evento is None:
        raise EventoNotFound(clave_evento)

    asistente = await buscar_asistente(db, correo, clave_evento)

    if asistente is None:
        raise AsistenteNotFound(correo)

    t = templates.get_template(evento.template)

    result = t.render(
        asistente=asistente.nombre_completo,
        folio=asistente.folio,
        name_class="nombre-largo"
        if len(asistente.nombre_completo.replace(" ", "").strip()) > 20
        else "nombre-chico",
        request=request,
    )

    html_doc = HTML(
        string=result,
        base_url="backend/static",
    )

    pdf = html_doc.write_pdf()

    await _update_asistente(
        db,
        asistente.clave,
        AsistenteUpdate(ya_descargo=True),
        clave_evento=clave_evento,
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="constancia-{asistente.folio}.pdf"'
        },
    )
