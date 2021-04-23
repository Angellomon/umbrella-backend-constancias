from datetime import datetime
from typing import Optional

from pydantic import BaseModel, AnyHttpUrl


class Scopes(BaseModel):
    CREATE_ASISTENTES: str = "create:asistentes"
    READ_ASISTENTES: str = "read:asistentes"
    UPDATE_ASISTENTES: str = "update:asistentes"
    DELETE_ASISTENTES: str = "delete:asistentes"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    iss: Optional[AnyHttpUrl]
    sub: str  # * clave de usuario
    exp: datetime
    iat: datetime

    scopes: list[str] = []
