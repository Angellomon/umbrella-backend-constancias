from io import BytesIO
from typing import Optional
from backend.core.pdf.canvas import Fonts, get_canvas
from backend.core.pdf.writer import (
    get_pdf,
    get_pdf_template,
    merge_pdf_template,
    replace_text_in_pdf,
)


def generar_pdf_constancia(
    folio: str, nombre_asistente: str, template: str, replace_text: bool = False
):
    packet_folio = BytesIO()
    pdf_template = get_pdf_template(template)  # type:ignore
    replace_text = True

    if replace_text:
        pdf_name_replace = replace_text_in_pdf(pdf_template, "NOMBREPERSONA")
        pdf_folio = replace_text_in_pdf(pdf_name_replace, "NUMFOLIO")
        pdf_final = merge_pdf_template(pdf_name_replace, pdf_folio)
    else:
        canvas_folio = get_canvas(
            font_size=55, font=Fonts.MONTSERRAT_BOLD_ITALIC, packet=packet_folio
        )

        canvas_folio.drawString(30, 180, f"# {folio}")

        canvas_folio.save()

        packet_folio.seek(0)

        packet_nombre = BytesIO()

        canvas_nombre = get_canvas(
            font_size=75, font=Fonts.MONTSERRAT_BOLD_ITALIC, packet=packet_nombre
        )

        canvas_nombre.drawCentredString(
            950, 630, nombre_asistente.upper().replace("  ", " ")
        )

        canvas_nombre.save()

        packet_nombre.seek(0)

        pdf_canvas_folio = get_pdf(initial_packet=packet_folio)
        pdf_canvas_nombre = get_pdf(initial_packet=packet_nombre)

        # pdf_text_replace = replace_text_in_pdf(pdf_template, "")

        res_folio = merge_pdf_template(pdf_canvas_nombre, pdf_template)
        pdf_folio = get_pdf(initial_packet=res_folio)

        pdf_final = merge_pdf_template(pdf_canvas_folio, pdf_folio)

    # res_template = replace_text_in_pdf(pdf_template, nombre_asistente)

    return pdf_final
