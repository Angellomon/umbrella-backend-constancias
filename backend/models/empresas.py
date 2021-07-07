from typing import Optional
from pydantic import BaseModel

from ..core.claves import generar_clave


class _EmpresaBase(BaseModel):
    clave: str = generar_clave()
    nombre: str
    detalles: str


class Empresa(_EmpresaBase):
    ...


class EmpresaCreate(BaseModel):
    nombre: str
    detalles: str = ""


class EmpresaUpdate(BaseModel):
    nombre: Optional[str] = None
    detalles: Optional[str] = None
