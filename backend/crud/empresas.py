from typing import Awaitable, List, Optional
from pydantic.errors import DataclassTypeError
from ..models.empresas import Empresa, EmpresaCreate, EmpresaUpdate

from ..db.mongodb import Database


async def buscar_empresa(
    db: Database, /, nombre: Optional[str] = None
) -> Optional[Empresa]:
    query = {}

    if nombre is not None:
        query["nombre"] = nombre

    empresa_doc = await db.empresas.find_one(query)

    return Empresa(**empresa_doc) if empresa_doc else None


async def crear_empresa(db: Database, /, empresa_data: EmpresaCreate) -> Empresa:
    assert (
        await buscar_empresa(db, empresa_data.nombre) is None
    ), f"empresa ya existente (nombre={empresa_data.nombre})"

    empresa = Empresa(**empresa_data.dict())

    await db.empresas.insert_one(empresa.dict())

    return empresa


async def get_empresa(db: Database, /, clave_empresa: str) -> Optional[Empresa]:
    empresa_doc = await db.empresas.find_one({"clave": clave_empresa})

    return Empresa(**empresa_doc) if empresa_doc else None


async def get_empresas(db: Database) -> List[Empresa]:
    cursor = db.empresas.find({})

    empresas = []

    async for doc in cursor:
        empresas.append(Empresa(**doc))

    return empresas


async def update_empresa(
    db: Database, clave_empresa: str, empresa_data: EmpresaUpdate
) -> Optional[Empresa]:
    empresa_doc = await db.empresas.find_one_and_update(
        {"clave": clave_empresa}, {"$set": empresa_data.dict(exclude_none=True)}
    )

    return Empresa(**empresa_doc) if empresa_doc else None


async def delete_empresa(db: Database, /, clave_empresa: str) -> Optional[Empresa]:
    empresa_doc = await db.empresas.find_one_and_delete({"clave": clave_empresa})

    return Empresa(**empresa_doc) if empresa_doc else None
