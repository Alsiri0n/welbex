from typing import TYPE_CHECKING
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .cargo import CargoSchema
    from .truck import TruckBase


class LocationSchema(BaseModel):
    town: str
    state: str
    zip: int = Field(gt=600, lt=99999)
    lat: float = Field(gt=-180, lt=180)
    lng: float = Field(gt=-180, lt=180)


class LocationInDB(LocationSchema):
    id: int | None = None

    class Config:
        orm_mode = True
