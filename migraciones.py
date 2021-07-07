from motor.motor_asyncio import AsyncIOMotorClient

from backend.models.asistentes import Asistente, AsistentesAlta
import asyncio
from backend.db.utils import connect, disconnect
from backend.db.mongodb import get_database
from backend.crud.asistentes import crear_asistentes


async def main():
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


if __name__ == "__main__":
    asyncio.run(main())
