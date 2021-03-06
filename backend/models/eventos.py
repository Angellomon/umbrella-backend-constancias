from typing import Literal, Optional
from pydantic import BaseModel, Field

from ..core.claves import generar_clave


class _EventoBase(BaseModel):
    clave: str = Field(default_factory=lambda: generar_clave())
    nombre: str
    inicio_folio: int = 1
    total_asistentes: int = 0
    espacios: int = 4
    clave_empresa: Optional[str] = None
    template: str = ""


class Evento(_EventoBase):
    @property
    def siguiente_folio(self):
        self.total_asistentes += 1
        return f"{self.total_asistentes}".zfill(self.espacios)


class EventoCreate(BaseModel):
    nombre: str
    inicio_folio: int = 1
    espacios: int = 4
    clave_empresa: Optional[str] = None
    template: str = ""


class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    inicio_folio: Optional[int] = None
    espacios: Optional[str] = None
    clave_empresa: Optional[str] = None
    total_asistentes: Optional[int] = None
    template: Optional[str] = None
