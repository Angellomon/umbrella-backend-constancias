from typing import Literal, Optional
from pydantic import BaseModel, Field
from backend.core.pdf.canvas import Fonts

from backend.core.pdf.writer import replace_text

from ..core.claves import generar_clave


class TextPositions(BaseModel):
    folio: list[int]
    nombre: list[int]


class TextOptions(BaseModel):
    font_size: int
    font: Fonts = Fonts.MONTSERRAT_BOLD_ITALIC
    position: list[int]
    chars_before: str = ""

    words_linebreak: Optional[int] = None
    vertical_spacing: int = 32

    hex_color: str = "#000000"


class RenderSettings(BaseModel):
    folio: TextOptions = TextOptions(
        font_size=55,
        position=[30, 180],
        chars_before="#",
    )
    nombre: TextOptions = TextOptions(font_size=75, position=[950, 630])


class _EventoBase(BaseModel):
    clave: str = Field(default_factory=lambda: generar_clave())
    nombre: str
    inicio_folio: int = 1
    total_asistentes: int = 0
    espacios: int = 4
    clave_empresa: Optional[str] = None
    template: str = ""

    replace_text: bool = False
    render_settings: RenderSettings = RenderSettings()


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
    render_settings: RenderSettings = RenderSettings()


class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    inicio_folio: Optional[int] = None
    espacios: Optional[str] = None
    clave_empresa: Optional[str] = None
    total_asistentes: Optional[int] = None
    template: Optional[str] = None

    replace_text: Optional[bool] = None
    render_settings: Optional[RenderSettings] = None
