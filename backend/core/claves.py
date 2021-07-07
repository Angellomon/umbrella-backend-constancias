from nanoid import generate

from .config import get_settings

s = get_settings()


def generar_clave() -> str:
    return generate(alphabet=s.NANOID_ALPHA, size=s.NANOID_SIZE)
