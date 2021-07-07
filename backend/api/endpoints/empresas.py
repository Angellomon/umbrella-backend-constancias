from backend.core.errors import EmpresaNotFound
from typing import List
from fastapi import APIRouter, Depends, Security

from ..deps import Database, get_database, User, get_current_user
from ...models.empresas import Empresa, EmpresaCreate, EmpresaUpdate
from ...crud.empresas import crear_empresa as _crear_empresa
from ...crud.empresas import get_empresa as _get_empresa
from ...crud.empresas import get_empresas as _get_empresas
from ...crud.empresas import update_empresa as _update_empresa
from ...crud.empresas import delete_empresa as _delete_empresa

router = APIRouter(tags=["Empresas"])


@router.post("/", response_model=Empresa)
async def crear_empresa(
    empresa_data: EmpresaCreate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    empresa = await _crear_empresa(db, empresa_data)

    return empresa


@router.get("/", response_model=List[Empresa])
async def get_empresas(
    db: Database = Depends(get_database), user: User = Security(get_current_user)
):
    empresas = await _get_empresas(db)

    return empresas


@router.get("/{clave_empresa}", response_model=Empresa)
async def get_empresa(
    clave_empresa: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    empresa = await _get_empresa(db, clave_empresa)

    if empresa is None:
        raise EmpresaNotFound(clave_empresa)

    return empresa


@router.patch("/{clave_empresa}", response_model=Empresa)
async def update_empresa(
    clave_empresa: str,
    empresa_data: EmpresaUpdate,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    empresa = await _update_empresa(db, clave_empresa, empresa_data)

    if empresa is None:
        raise EmpresaNotFound(clave_empresa)

    return empresa


@router.delete("./{clave_empresa}", response_model=Empresa)
async def delete_empresa(
    clave_empresa: str,
    db: Database = Depends(get_database),
    user: User = Security(get_current_user),
):
    empresa = await _delete_empresa(db, clave_empresa)

    if empresa is None:
        raise EmpresaNotFound(clave_empresa)

    return empresa
