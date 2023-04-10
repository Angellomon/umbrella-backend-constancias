import sys
from enum import Enum

from PyPDF2 import PdfFileReader, PdfReader, PdfWriter
from typing import Any, Dict, Optional, Union

import io

from PyPDF2.generic import (
    ArrayObject,
    ContentStream,
    DecodedStreamObject,
    EncodedStreamObject,
    IndirectObject,
    NameObject,
    PdfObject,
)


class Templates(str, Enum):
    COMECARNE_2022_COLOMBIA_NL_FILE = "constancia-comecarne-2022-colombia.pdf"


TEMPLATES_DIR = f"{sys.path[0]}/backend/templates"


def get_pdf_template(
    template: Templates, *, initial_packet: Optional[io.BytesIO] = None
):
    if initial_packet is None:
        initial_packet = io.BytesIO()

    tempalte_path = f"{TEMPLATES_DIR}/{template}"
    # tempalte_path = f"/home/angel/Documents/test.pdf"

    return PdfFileReader(open(tempalte_path, "rb"), strict=False)


def get_pdf(*, initial_packet: io.BytesIO = io.BytesIO()):
    return PdfReader(initial_packet)


def normalize_text(s: str, chars: str = "[]{}() :123456789."):
    for c in chars:
        s = s.replace(c, "")
    return s.replace("TJ", "").replace("Tj", "").replace("tj", "")


def replace_text(content: Any, replacements: dict[str, str] = dict()):
    lines: list[str] = content.splitlines()

    result = ""
    in_text = False

    for line in lines:
        if line == "BT":
            in_text = True

        elif line == "ET":
            in_text = False

        elif in_text:
            cmd = line[-2:]
            if cmd.lower() == "tj":
                replaced_line = normalize_text(line)

                if not replaced_line in replacements:
                    result += line + "\n"

                    continue

                result += replacements[replaced_line] + "\n"

                # for k, v in replacements.items():
                #     replaced_line = replaced_line.replace(k, v)

                # print(replaced_line)

                # result += replaced_line + "\n"
            else:
                result += line + "\n"

            continue

        result += line + "\n"

    return result


def process_data(
    pdf_content: Union[ContentStream, EncodedStreamObject], contents: dict[str, str]
):
    print(type(pdf_content))
    print(dir(pdf_content))

    data = pdf_content.get_data()

    if data is None:
        return

    if isinstance(data, str):
        decoded_data = data.encode("utf-8")
    else:
        decoded_data = data.decode("utf-8")

    replaced_data = replace_text(decoded_data, contents)
    # print("---")
    # print(replaced_data)
    # print("---")
    encoded_data = replaced_data.encode("utf-8")

    if pdf_content.decodedSelf is not None:
        pdf_content.decodedSelf.set_data(encoded_data)
    else:
        pdf_content.set_data(encoded_data)


def replace_text_in_pdf(pdf: PdfReader, contents: dict[str, str]):
    result = PdfWriter()
    b = io.BytesIO()
    b.seek(0)

    print(id(pdf.pages[0]))

    page_pdf = pdf.pages[0]

    result.add_blank_page(page_pdf.mediabox[2], page_pdf.mediabox[3])
    # result.add_page(page_pdf)

    # page = result.pages[1]
    page = page_pdf

    page_contents = page.get_contents()

    assert page_contents is not None, "no hay contenido @replace_text_in_pdf()"

    # print(page_contents)

    if isinstance(page_contents, DecodedStreamObject) or isinstance(
        page_contents, EncodedStreamObject
    ):
        process_data(page_contents, contents)
    else:
        for obj in page_contents:  # type: ignore
            if (
                # isinstance(obj, DecodedStreamObject)
                # or isinstance(obj, EncodedStreamObject)
                isinstance(obj, IndirectObject)
            ):
                streamObj: EncodedStreamObject = obj.getObject()  # type: ignore

                if streamObj is None:
                    continue

                process_data(streamObj, contents)

    if isinstance(page_contents, (ArrayObject, list)):
        # print(id(pdf.pages[0][NameObject("/Contents")]))

        page[NameObject("/Contents")] = page_contents

        print([f"{c.getObject().get_data().decode()[-50:]}\n" for c in page_contents])
    else:
        page[NameObject("/Contents")] = page_contents.decodedSelf

    # result = PdfWriter()
    # b = io.BytesIO()
    # b.seek(0)
    # # page.write_to_stream(b, None)

    # result.add_blank_page(int(page.mediabox[2]), int(page.mediabox[3]))

    # result.add_page(pdf.pages[0])
    # print(result.pages[0] == pdf.pages[0])
    # result.add_blank_page(int(page.mediabox[2]), int(page.mediabox[3]))
    # result.pages[1].merge_page(pdf.pages[0])

    result.pages[0][NameObject("/Contents")] = page.get_contents()

    print(
        f"[178] {[content.getObject().get_data().decode()[-50:] for content in page[NameObject('/Contents')]]}\n"
    )
    # print(id(result.pages[0][NameObject("/Contents")]))

    # print(result.pages[0][NameObject("/Contents")])

    result.add_page(page)
    print(
        [
            f"[183] {c.getObject().get_data().decode()[-50:]}\n"
            for c in page.get_contents()
        ]
    )
    print("-" * 30)
    # print(dir(page.get_object()["/Parent"]["/Kids"][0].get_object()))
    from loguru import logger

    logger.debug(page)

    # BUG: old data is being written on result
    result.write(b)

    # pdf_test = PdfReader(pdf)

    # print(f"\nid pdf.pages {id(page)}")
    # print(f"\nid pdf.pages[0].get_content() {id(page.get_contents())}")
    # print(
    #     f"id pdf.pages[0][NameObject('/Contents')]: {id(pdf.pages[0][NameObject('/Contents')])}"
    # )
    # print(
    #     f"pdf {[content.getObject().get_data().decode()[-50:] for content in pdf.pages[0].get_contents()]}\n"
    # )

    # print(f"id result.pages {id(result.pages)}")
    # print(f"id result.pages[0].get_contents(): {id(result.pages[0].get_contents())}")
    # print(
    #     f"id result.pages[0][NameObject('/Contents')]: {id(result.pages[0][NameObject('/Contents')])}"
    # )
    # print(
    #     f"result {[content.getObject().get_data().decode()[-50:] for content in result.pages[0].get_contents()]}\n"
    # )

    # print(f"id PdfReader(b).pages[0]: {id(PdfReader(b).pages[0])}")
    # print(
    #     f"id PdfReader(b).pages[0].get_contents(): {id(PdfReader(b).pages[0].get_contents())}"
    # )
    # print(
    #     f"id PdfReader(b).pages[0][NameObject('/Contents')]: {id(PdfReader(b).pages[0][NameObject('/Contents')])}"
    # )
    # print(
    #     f"carga b (result.write(b)) [...{[content.getObject().get_data().decode()[-50:] for content in PdfReader(b).pages[0][NameObject('/Contents')]]}]\n"
    # )
    # # print(result.pages[0].getContents()[-1].getObject().get_data().decode())
    # # print("----------")
    # print(pdf.stream.read()[-50:])

    return b


def merge_pdf_template(pdf_canvas: PdfReader, pdf_template: PdfReader):
    pdf_result = PdfWriter()

    page_canvas = pdf_canvas.pages[0]
    page_template = pdf_template.pages[0]

    page_template.mergePage(page_canvas)

    pdf_result.addPage(page_template)

    buffer = io.BytesIO()
    buffer.seek(0)

    pdf_result.write(buffer)

    return buffer
