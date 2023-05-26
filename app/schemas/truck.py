from pydantic import BaseModel, Field
from app.schemas.location import LocationInDB


class TruckBase(BaseModel):
    number: str = Field(max_length=5)
    capacity: int = Field(ge=1, le=1000)

    location_id: int


class TruckInDB(TruckBase):
    id: int
    number: str = Field(max_length=5)
    capacity: int = Field(ge=1, le=1000)

    location_id: int
    location: LocationInDB

    class Config:
        orm_mode = True


class Truck(TruckInDB):
    pass


class TruckForInformation(BaseModel):
    number: str = Field(max_length=5)
    distance: int
