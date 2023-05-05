from fastapi import APIRouter, Depends, Response
from pydantic import EmailStr
from backend.core.errors import AsistenteNotFound, EventoNotFound
from backend.crud.asistentes import buscar_asistente, update_asistente

from backend.db.mongodb import Database, get_database
from backend.core.constancias import generar_pdf_constancia_bytes
from PyPDF2 import PdfReader

from backend.models.asistentes import AsistenteUpdate

from ...crud.eventos import get_evento as _get_evento

router = APIRouter()


@router.get("/{clave_evento}")
async def obtener_pdf_asistente(
    clave_evento: str, correo: EmailStr, db: Database = Depends(get_database)
):
    evento = await _get_evento(db, clave_evento)

    if evento is None:
        raise EventoNotFound(clave_evento)

    asistente = await buscar_asistente(db, correo, clave_evento)

    if asistente is None:
        raise AsistenteNotFound(correo)

    resultado = generar_pdf_constancia_bytes(asistente, evento)

    resultado.seek(0)

    r = resultado.read()

    await update_asistente(db, asistente.clave, AsistenteUpdate(ya_descargo=True))

    return Response(
        content=r,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="constancia-{asistente.folio}.pdf"'
        },
    )
