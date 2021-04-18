from loguru import logger
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from weasyprint import HTML

from .deps import get_templates

router = APIRouter()


@router.get("/")
async def test(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    t = templates.get_template("test-pdf.html")
    result = t.render(
        interest_rate=0.34, names=["angel", "angel malvado"], request=request
    )

    html_doc = HTML(
        string=result,
        base_url="backend/static",
    )

    pdf = html_doc.write_pdf()

    logger.debug(type(pdf))

    return Response(content=pdf, media_type="application/pdf")
