from loguru import logger
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from weasyprint import HTML

from ...models.asistentes import Asistente
from .deps import get_templates

router = APIRouter()

asistentes = [
    Asistente(
        folio="0001",
        primer_nombre="Angel",
        apellido_p="Martínez",
        apellido_m="Díaz",
        correo="angelmtzdiaz@gmail.com",
    ),
    Asistente(
        folio="0002",
        primer_nombre="Angel",
        segundo_nombre="El Malvado",
        apellido_p="Martínez",
        apellido_m="Díaz",
        correo="angelmtzdiaz@gmail.com",
    ),
]


@router.get("/")
async def test(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    t = templates.get_template("test-pdf.html")
    asistente = asistentes[1]
    result = t.render(
        asistente=asistente.nombre_completo,
        folio=asistente.folio,
        request=request,
    )

    html_doc = HTML(
        string=result,
        base_url="backend/static",
    )

    pdf = html_doc.write_pdf()

    logger.debug(type(pdf))

    return Response(content=pdf, media_type="application/pdf")
