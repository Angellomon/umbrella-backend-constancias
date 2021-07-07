from fastapi.exceptions import HTTPException
from fastapi import status


class EventoNotFound(Exception):
    def __init__(self, clave_evento: str) -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"evento no encontrado (clave={clave_evento})",
        )


class EmpresaNotFound(Exception):
    def __init__(self, clave_empresa: str) -> None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"empresa no encontrada (clave={clave_empresa})",
        )
