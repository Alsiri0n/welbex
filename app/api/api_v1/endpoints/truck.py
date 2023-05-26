from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{id_}", response_model=schemas.Truck)
async def get_truck(*, db: AsyncSession = Depends(deps.get_db), id_: int):
    truck = await crud.truck.get(db, id_)
    return truck


@router.put("/{id_}", response_model=schemas.Truck)
async def update_truck(*, db: AsyncSession = Depends(deps.get_db), id_: int, location_zip: int):
    truck = await crud.truck.get(db, id_)
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    location = await crud.location.get(db, postcode=location_zip)
    if not location:
        raise HTTPException(status_code=404, detail="Location zip not found")
    truck = await crud.truck.update(db, id_=id_, location=location.id)
    return truck
