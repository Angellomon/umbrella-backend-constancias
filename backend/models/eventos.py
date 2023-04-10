from typing import Literal, Optional
from pydantic import BaseModel, Field

from ..core.claves import generar_clave


class TextPositions(BaseModel):
    folio: list[int]
    nombre: list[int]


class _EventoBase(BaseModel):
    clave: str = Field(default_factory=lambda: generar_clave())
    nombre: str
    inicio_folio: int = 1
    total_asistentes: int = 0
    espacios: int = 4
    clave_empresa: Optional[str] = None
    template: str = ""

    replace_text: bool = False
    text_positions: Optional[TextPositions] = None


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
    replace_text: bool = False


class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    inicio_folio: Optional[int] = None
    espacios: Optional[str] = None
    clave_empresa: Optional[str] = None
    total_asistentes: Optional[int] = None
    template: Optional[str] = None
    replace_text: Optional[bool] = None
    text_positions: Optional[TextPositions] = None
