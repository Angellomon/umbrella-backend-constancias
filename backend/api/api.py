from fastapi import APIRouter

from .endpoints.asistentes import router as asistentes_router
from .endpoints.eventos import router as eventos_router
from .endpoints.oauth import router as oauth_router
from .endpoints.users import router as usuarios_router

router = APIRouter()


router.include_router(asistentes_router, prefix="/asistentes")
router.include_router(usuarios_router, prefix="/users")
router.include_router(oauth_router, prefix="/oauth")
router.include_router(eventos_router, prefix="/eventos")
