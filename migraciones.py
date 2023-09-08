import io
from motor.motor_asyncio import AsyncIOMotorClient

from backend.models.asistentes import Asistente, AsistentesAlta
import asyncio
from backend.db.utils import connect, disconnect
from backend.db.mongodb import get_database
from backend.crud.asistentes import crear_asistentes


async def test():
    CLAVE_EVENTO = "d02mbve0yy"
    client = AsyncIOMotorClient("mongodb+srv://dev:passtest@cluster0.oju78.mongodb.net")

    cursor = client["NAEQUINA"]["asistentes"].find()

    asistentes = []

    async for doc in cursor:
        asistentes.append(Asistente(clave_evento=CLAVE_EVENTO, **doc))

    print(asistentes)

    await connect()

    db = get_database()

    await crear_asistentes(
        db,
        CLAVE_EVENTO,
        AsistentesAlta(asistentes=asistentes, clave_evento=CLAVE_EVENTO),
    )

    await disconnect()


async def test_get_canvas():
    from backend.core.pdf.canvas import get_canvas

    canvas = get_canvas()

    print(canvas)


async def test_get_pdf_template():
    from backend.core.pdf.canvas import get_canvas
    from backend.core.pdf.writer import get_pdf_template, Templates

    packet = io.BytesIO()

    canvas = get_canvas(packet=packet)

    canvas.drawString(10, 100, "Hello world")
    canvas.save()

    pdf = get_pdf_template(
        Templates.COMECARNE_2022_COLOMBIA_NL_FILE, initial_packet=packet
    )

    print(pdf)


async def convert_email_to_lowercase():
    from loguru import logger

    CLAVE_EVENTO = "hmmm"
    client = AsyncIOMotorClient("mongodb+srv://ayyy:lmao@cluster.mongodb.net")

    db = client["CONSTANCIAS"]["asistentes"]

    cursor = db.find({"clave_evento": CLAVE_EVENTO})

    asistentes = []

    async for doc in cursor:
        asistentes.append({"id": doc["_id"], "correo": doc["correo"]})

    logger.debug(asistentes)

    for asistente in asistentes:
        await db.update_one(
            {"_id": asistente["id"]}, {"$set": {"correo": asistente["correo"].lower()}}
        )

        logger.debug(f"updated: {asistente} with {asistente['correo'].lower()}")

    logger.debug("finished")


async def _main():
    await convert_email_to_lowercase()


if __name__ == "__main__":
    asyncio.run(_main())
