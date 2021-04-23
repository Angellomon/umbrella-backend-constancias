from typing import Optional
from pydantic import BaseModel, EmailStr


class AsistenteBase(BaseModel):
    folio: str
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    apellido_p: str
    apellido_m: str
    correo: EmailStr

    @property
    def nombre_completo(self) -> str:
        apellidos = f"{self.apellido_p} {self.apellido_m}"
        return (
            f"{self.primer_nombre} {self.segundo_nombre} {apellidos}"
            if self.segundo_nombre
            else f"{self.primer_nombre} {apellidos}"
        )


class Asistente(AsistenteBase):
    ...


class AsistenteCreate(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    apellido_p: str
    apellido_m: str
    correo: EmailStr


class AsistenteUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    apellido_p: Optional[str] = None
    apellido_m: Optional[str] = None
    correo: Optional[EmailStr] = None
