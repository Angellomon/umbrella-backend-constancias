from datetime import datetime, timedelta
from typing import Dict

from jose import jwt

from .config import get_settings

ALGORITHM = "HS256"

settings = get_settings()


def create_access_token(data: Dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "aud": settings.SERVER_NAME,
            "iss": settings.SERVER_HOST,
            "exp": expire.timestamp(),
            "iat": datetime.now().timestamp(),
        }
    )
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
