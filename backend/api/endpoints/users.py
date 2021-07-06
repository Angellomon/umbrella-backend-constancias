from backend.core.oauth import get_scopes
from fastapi import APIRouter, Security, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends

from ....crud.users import create_user as _create_user
from ....crud.users import get_user as _get_user
from ....db.mongodb import Database, get_database
from ....models.users import User, UserCreate
from ..deps import get_current_user

router = APIRouter(tags=["Usuarios"])
s = get_scopes()


@router.post("/", response_model=User)
async def create_user(
    usuario_data: UserCreate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.CREATE_USER]),
):
    usuario = await _create_user(db, usuario_data)

    return usuario


@router.get("/{username}", response_model=User)
async def get_usuario(
    username: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user, scopes=[s.READ_USERS]),
):
    usuario = await _get_user(db, username)

    if usuario is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"usuario no encontrado (username={username})",
        )

    return usuario
