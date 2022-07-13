import io
import sys
from enum import Enum
from typing import Optional

import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape


class Fonts(str, Enum):
    MONTSERRAT_BOLD_ITALIC = "Montserrat Bold Italic"
    MONTSERRAT_BOLD_ITALIC_FILE = 'montserrat-bold-italic.ttf'


FONTS_DIR = sys.path[0]


reportlab.rl_config.TTFSearchPath.append(str(FONTS_DIR) + '/backend/static/fonts')
pdfmetrics.registerFont(TTFont(Fonts.MONTSERRAT_BOLD_ITALIC, Fonts.MONTSERRAT_BOLD_ITALIC_FILE))


def get_canvas(*, font_size: int = 15, font: Fonts = Fonts.MONTSERRAT_BOLD_ITALIC, packet: Optional[io.BytesIO] = None):
    if packet is None:
        packet = io.BytesIO()

    c = canvas.Canvas(packet, pagesize=landscape((5000, 6000)))

    c.setFont(font, font_size)

    return c
