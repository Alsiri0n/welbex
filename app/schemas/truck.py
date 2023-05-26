from pydantic import BaseModel, Field


class TruckBase(BaseModel):
    id: int
    number: str = Field(max_length=5)
    capacity: int = Field(gt=1, lt=1000)

    location_id: int


class TruckInDB(TruckBase):
    id: int
    number: str = Field(max_length=5)
    capacity: int = Field(gt=1, lt=1000)

    location_id: int

    class Config:
        orm_mode = True


class Truck(TruckInDB):
    pass
