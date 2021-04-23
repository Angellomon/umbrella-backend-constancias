from datetime import datetime

from pydantic import BaseModel


class Scopes(BaseModel):
    CREATE_ASISTENTES: str = "create:asistentes"
    READ_ASISTENTES: str = "read:asistentes"
    UPDATE_ASISTENTES: str = "update:asistentes"
    DELETE_ASISTENTES: str = "delete:asistentes"

    CREATE_USER: str = "create:user"
    READ_USERS: str = "read:users"
    UPDATE_USER: str = "update:user"
    DELETE_USER: str = "delete:user"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    # iss: Optional[AnyHttpUrl]
    sub: str  # * clave de usuario
    exp: datetime
    iat: datetime

    scopes: list[str] = []
