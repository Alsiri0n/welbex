from pydantic import BaseModel, Field


class CargoSchema(BaseModel):
    id: int
    weight: int = Field(gt=1, lt=1000)
    description: str

    pickup_id: int
    delivery_id: int
