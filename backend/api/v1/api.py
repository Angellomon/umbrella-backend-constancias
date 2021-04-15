from fastapi import APIRouter

from .deps import get_settings

router = APIRouter()


@router.get("/")
async def test():
    settings = get_settings()
    return {"message": f"hello {settings.PROJECT_NAME}"}
