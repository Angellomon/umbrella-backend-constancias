from io import BytesIO
from typing import Optional

from PyPDF2 import PdfReader
from backend.core.pdf.canvas import Fonts, get_canvas
from backend.core.pdf.writer import (
    get_pdf,
    get_pdf_template,
    merge_pdf_template,
    replace_text_in_pdf,
)
from backend.models.asistentes import Asistente
from backend.models.eventos import Evento


# BUG: in replace_text opt (new pdf clones data from old doc)
def generar_pdf_constancia_bytes(asistente: Asistente, evento: Evento):
    pdf_template = get_pdf_template(evento.template)  # type:ignore
    # replace_text = True

    if evento.replace_text:
        pdf_final_bytes = replace_text_in_pdf(
            pdf_template, {"NOMBREPERSONA": "", "NUMFOL": ""}
        )

        pdf_test = PdfReader(pdf_final_bytes)
        # print(
        #     f"{[content.getObject().get_data().decode() for content in pdf_test.getPage(0).getContents()]}"
        # )

    else:

        folio_settings = evento.render_settings.folio
        nombre_settings = evento.render_settings.nombre

        packet_folio = BytesIO()
        canvas_folio = get_canvas(
            font_size=folio_settings.font_size,
            font=folio_settings.font,
            packet=packet_folio,
        )

        if folio_settings.chars_before:
            folio = f"{folio_settings.chars_before} {asistente.folio}".strip()
        else:
            folio = asistente.folio.strip()

        canvas_folio.drawString(
            folio_settings.position[0], folio_settings.position[1], folio
        )
        canvas_folio.save()
        packet_folio.seek(0)

        packet_nombre = BytesIO()
        canvas_nombre = get_canvas(
            font_size=nombre_settings.font_size,
            font=nombre_settings.font,
            packet=packet_nombre,
        )

        canvas_nombre.drawCentredString(
            nombre_settings.position[0],
            nombre_settings.position[1],
            asistente.nombre_completo,
        )
        canvas_nombre.save()
        packet_nombre.seek(0)

        pdf_canvas_folio = get_pdf(initial_packet=packet_folio)
        pdf_canvas_nombre = get_pdf(initial_packet=packet_nombre)

        # pdf_text_replace = replace_text_in_pdf(pdf_template, "")

        res_folio = merge_pdf_template(pdf_canvas_nombre, pdf_template)
        pdf_folio = get_pdf(initial_packet=res_folio)
        pdf_final_bytes = merge_pdf_template(pdf_canvas_folio, pdf_folio)

    # res_template = replace_text_in_pdf(pdf_template, nombre_asistente)

    # pdf_test = PdfReader(pdf_final_bytes)
    # print(
    #     f"{[content.getObject().get_data().decode() for content in pdf_test.getPage(0).getContents()]}"
    # )
    return pdf_final_bytes
