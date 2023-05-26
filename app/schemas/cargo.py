from pydantic import BaseModel, Field
from app.schemas.location import LocationInDB
from app.schemas.truck import TruckForInformation


class CargoBase(BaseModel):
    weight: int = Field(ge=1, le=1000)
    description: str

    pickup_id: int
    delivery_id: int


class CargoInDB(CargoBase):
    id: int
    weight: int = Field(ge=1, le=1000)
    description: str

    pickup_id: int
    delivery_id: int

    pickup: LocationInDB
    delivery: LocationInDB

    class Config:
        orm_mode = True


class Cargo(CargoInDB):
    pass


class CargoWithQntTrucks(CargoInDB):
    truck_qnt: int


class CargoWithDistanceTruck(CargoInDB):
    trucks: list[TruckForInformation]