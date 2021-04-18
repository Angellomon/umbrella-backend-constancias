import jinja2

from ..config import get_settings

from functools import lru_cache

settings = get_settings()


@lru_cache
def get_template_env() -> jinja2.Environment:
    template_loader = jinja2.FileSystemLoader(searchpath=settings.STATIC_DIR)

    return jinja2.Environment(loader=template_loader)


@lru_cache
def get_template(template: str) -> jinja2.Template:
    template_env = get_template_env()

    return template_env.get_template(template)
