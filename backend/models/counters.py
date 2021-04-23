from pydantic import BaseModel
from enum import Enum


class Entidades(str, Enum):
    asistentes = "asistentes"


class EntityCounter(BaseModel):
    clave: str
    valor: int = 0
