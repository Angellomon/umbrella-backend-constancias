import secrets
from typing import Tuple

import bcrypt
from passlib.context import CryptContext

from .config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"
access_token_jwt_subject = "access"

settings = get_settings()


def generate_salt() -> str:
    return bcrypt.gensalt().decode()


def generate_client_credentials() -> Tuple[str, str]:
    return secrets.token_urlsafe(16), secrets.token_urlsafe(32)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
