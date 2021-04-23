from functools import lru_cache

from ..models.oauth import Scopes


@lru_cache
def get_scopes() -> Scopes:
    return Scopes()


def gen_admin_scopes() -> list[str]:
    s = get_scopes()

    scopes = []

    for _, value in s:
        scopes.append(value)

    return scopes
