from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic, OAuth2PasswordRequestForm
from loguru import logger

from ...core.jwt import create_access_token
from ...crud.users import authenticate_user
from ...db.mongodb import Database, get_database
from ...models.oauth import Token

router = APIRouter()

basic_auth = HTTPBasic()


@router.post("/token", response_model=Token, tags=["Autenticación"])
async def login(
    db: Database = Depends(get_database),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """login del usuario"""

    user = await authenticate_user(
        db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="usuario y/o contraseña no válidos"
        )

    access_token = create_access_token({"sub": user.username, "scopes": user.scopes})

    logger.info(f"access token issued (username={user.username})")

    return Token(access_token=access_token, token_type="bearer")
