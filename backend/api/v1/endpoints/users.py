from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from ....models.users import User, UserCreate
from ....db.mongodb import Database, get_database

from ....crud.users import create_user as _create_user, get_user as _get_user

router = APIRouter(tags=["Usuarios"])


@router.post("/", response_model=User)
async def create_user(usuario_data: UserCreate, db: Database = Depends(get_database)):
    usuario = await _create_user(db, usuario_data)

    return usuario


@router.get("/{username}", response_model=list[User])
async def get_usuario(username: str, db: Database = Depends(get_database)):
    usuario = await _get_user(db, username)

    if usuario is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"usuario no encontrado (username={username})",
        )

    return usuario
