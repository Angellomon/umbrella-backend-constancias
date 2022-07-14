import sys
from enum import Enum

from PyPDF2 import PdfFileReader, PdfReader, PdfWriter
from typing import Any, Dict, Optional

import io

from PyPDF2.generic import ArrayObject, DecodedStreamObject, EncodedStreamObject, IndirectObject, NameObject


class Templates(str, Enum):
    COMECARNE_2022_COLOMBIA_NL_FILE = "constancia-comecarne-2022-colombia.pdf"


TEMPLATES_DIR = f"{sys.path[0]}/backend/templates"


def get_pdf_template(template: Templates, *, initial_packet: Optional[io.BytesIO] = None):
    if initial_packet is None:
        initial_packet = io.BytesIO()

    tempalte_path = f"{TEMPLATES_DIR}/{template}"

    return PdfFileReader(open(tempalte_path, "rb"), strict=False)


def get_pdf(*, initial_packet: io.BytesIO = io.BytesIO()):
    return PdfReader(initial_packet)


def replace_text(content: Any, replacements: Dict = dict()):
    lines = content.splitlines()

    result = ""
    in_text = False

    for line in lines:
        if line == "BT":
            in_text = True

        elif line == "ET":
            in_text = False

        elif in_text:
            cmd = line[-2:]
            if cmd.lower() == 'tj':
                replaced_line = line
                for k, v in replacements.items():
                    replaced_line = replaced_line.replace(k, v)
                result += replaced_line + "\n"
            else:
                result += line + "\n"
            continue

        result += line + "\n"

    return result


def process_data(pdf_content: Any, s: str):
    data = pdf_content.get_data()

    decoded_data = data.decode('utf-8')

    replaced_data = replace_text(decoded_data, {
        "NOMBRE": s
    })

    encoded_data = replaced_data.encode('utf-8')
    if pdf_content.decodedSelf is not None:
        pdf_content.decodedSelf.setData(encoded_data)
    else:
        pdf_content.setData(encoded_data)


def replace_text_in_pdf(pdf: PdfReader, new_text: str):
    result = PdfWriter()

    page = pdf.getPage(0)

    contents = page.getContents()

    assert contents is not None, "no hay contenido @replace_text_in_pdf()"

    if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
        process_data(contents, new_text)
    else:
        for obj in contents:  # type: ignore
            if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject) or isinstance(obj, IndirectObject):
                streamObj = obj.getObject()
                process_data(streamObj, new_text)

    if isinstance(contents, ArrayObject):
        page[NameObject("/Contents")] = contents
    else:
        page[NameObject("/Contents")] = contents.decodedSelf

    result.addPage(page)

    b = io.BytesIO()
    result.write(b)
    b.seek(0)

    return PdfReader(b)


def merge_pdf_template(pdf_canvas: PdfReader, pdf_template: PdfReader):
    pdf_result = PdfWriter()

    page_canvas = pdf_canvas.getPage(0)
    page_template = pdf_template.getPage(0)

    page_template.mergePage(page_canvas)

    pdf_result.addPage(page_template)

    buffer = io.BytesIO()
    buffer.seek(0)

    pdf_result.write(buffer)

    return buffer
