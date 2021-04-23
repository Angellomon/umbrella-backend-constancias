from functools import lru_cache

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.templating import Jinja2Templates
from jose import jwt
from jose.exceptions import JWTError
from loguru import logger

from ...core.config import Settings, get_settings
from ...core.oauth import get_scopes
from ...core.security import ALGORITHM
from ...crud.users import get_user
from ...db.mongodb import Database, get_database
from ...models.oauth import TokenPayload
from ...models.users import User

settings = get_settings()
s = get_scopes()

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.BASE_URL}/oauth/token",
    scopes={
        s.CREATE_ASISTENTES: "Puede crear asistentes",
        s.READ_ASISTENTES: "Puede consultar a los asistentes",
        s.UPDATE_ASISTENTES: "Puede actualizar asistentes",
        s.DELETE_ASISTENTES: "Puede eliminar asistentes",
    },
)


@lru_cache
def get_templates() -> Jinja2Templates:
    return Jinja2Templates(directory=get_settings().TEMPLATES_DIR)


async def get_current_user(
    security_scopes: SecurityScopes,
    db: Database = Depends(get_database),
    token: str = Depends(oauth_scheme),
) -> User:
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope={security_scopes.scope_str}"
    else:
        authenticate_value = "Bearer"

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=settings.PROJECT_NAME,
        )
        token_data = TokenPayload(**payload)
    except JWTError as error:
        logger.error(error)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="no se pudo validar las credenciales",
        )

    user = await get_user(db, username=token_data.sub)

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="permisos insuficientes",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


__all__ = ["Settings", "get_settings", "Database", "get_database"]
