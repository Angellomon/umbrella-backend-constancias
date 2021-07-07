from typing import Literal
from pydantic import BaseModel

from ..core.claves import generar_clave


class _EventoBase(BaseModel):
    clave: str = generar_clave()
    nombre: str
    inicio_folio: int = 1
    total_asistentes: int = 0
    espacios: int = 4


class Evento(_EventoBase):
    @property
    def siguiente_folio(self):
        self.total_asistentes += 1
        return f"{self.total_asistentes}".zfill(self.espacios)
