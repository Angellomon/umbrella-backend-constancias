from pydantic import BaseModel


class TestTemplate(BaseModel):
    interest_rate: float
    names: list[float]
