from pydantic import BaseModel, Field


class TruckSchema(BaseModel):
    id: int
    number: str = Field(max_length=5)
    capacity: int = Field(gt=1, lt=1000)

    location_id: int
