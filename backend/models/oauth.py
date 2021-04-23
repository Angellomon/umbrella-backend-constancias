from pydantic import BaseModel


class Scopes(BaseModel):
    CREATE_ASISTENTES: str = "create:asistentes"
    READ_ASISTENTES: str = "read:asistentes"
    UPDATE_ASISTENTES: str = "update:asistentes"
    DELETE_ASISTENTES: str = "delete:asistentes"
