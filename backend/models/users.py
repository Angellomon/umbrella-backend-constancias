from backend.core.oauth import gen_admin_scopes
from enum import Enum
from pydantic import BaseModel
from ..core.security import verify_password, generate_salt, get_password_hash


class Roles(str, Enum):
    admin = "admin"


class UserBase(BaseModel):
    username: str
    nombre: str
    role: Roles


class UserDB(UserBase):
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str) -> bool:
        return verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = generate_salt()
        self.hashed_password = get_password_hash(self.salt + password)


class User(UserBase):
    @property
    def scopes(self) -> list[str]:
        if self.role == Roles.admin:
            return gen_admin_scopes()
        return []
