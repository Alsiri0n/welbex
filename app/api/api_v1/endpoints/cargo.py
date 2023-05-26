from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=list[schemas.CargoWithQntTrucks])
async def all_cargos(*, db: AsyncSession = Depends(deps.get_db)):
    cargos = await crud.cargo.list_cargo(db)
    cargo_with_trucks = []
    for cur_cargo in cargos:
        qnt = await crud.truck.get_truck_by_distance(db, lat=cur_cargo.pickup.lat, lng=cur_cargo.pickup.lng, miles=450)
        cargo_with_trucks.append(schemas.CargoWithQntTrucks(
            id=cur_cargo.id,
            weight=cur_cargo.weight,
            description=cur_cargo.description,
            pickup_id=cur_cargo.pickup_id,
            delivery_id=cur_cargo.delivery_id,
            pickup=cur_cargo.pickup,
            delivery=cur_cargo.delivery,
            truck_qnt=qnt))
    return cargo_with_trucks


@router.get("/{id_}", response_model=schemas.CargoWithDistanceTruck)
async def get_cargo_info(*, db: AsyncSession = Depends(deps.get_db), id_: int):
    # Defaul get
    # cargo = await crud.cargo.get(db, id_)
    # if not cargo:
    #     raise HTTPException(status_code=404, detail="Cargo not found")
    # return cargo
    cargo = await crud.cargo.get(db, id_)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    information: list[schemas.TruckForInformation] = await crud.truck.get_distance(db,
                                                                                 lat=cargo.pickup.lat,
                                                                                 lng=cargo.pickup.lng)
    cargo: schemas.CargoWithDistanceTruck = schemas.CargoWithDistanceTruck(
        id=cargo.id,
        weight=cargo.weight,
        description=cargo.description,
        pickup_id=cargo.pickup_id,
        delivery_id=cargo.delivery_id,
        pickup=cargo.pickup,
        delivery=cargo.delivery,
        trucks=information
    )
    return cargo



@router.post("/", response_model=schemas.Cargo)
async def create_cargo(*, db: AsyncSession = Depends(deps.get_db),
                       zip_delivery: int,
                       zip_pickup: int,
                       weight: int = 0,
                       description: str = ""):
    if zip_delivery == zip_pickup:
        raise HTTPException(status_code=400, detail="Delivery and pickup match")

    if weight < 1:
        raise HTTPException(status_code=400, detail="Weight is wrong")

    pickup = await crud.location.get(db, zip_pickup)
    if not pickup:
        raise HTTPException(status_code=404, detail="Pickup zip code not found")

    delivery = await crud.location.get(db, zip_delivery)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery zip code not found")

    schema: schemas.CargoBase = schemas.CargoBase(
        weight=weight,
        description=description,
        pickup_id=pickup.id,
        delivery_id=delivery.id
    )
    cargo = await crud.cargo.create(db, schema)
    return cargo


@router.put("/{id_}", response_model=schemas.Cargo)
async def update_cargo(*, db: AsyncSession = Depends(deps.get_db), id_: int, weight: int, description: str = ""):
    if weight < 1:
        raise HTTPException(status_code=400, detail="Weight is wrong")
    cargo = await crud.cargo.get(db, id_)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    cargo = await crud.cargo.update(db, id_=id_, weight=weight, description=description)
    return cargo


@router.delete("/{id_}", response_model=schemas.Cargo)
async def delete_cargo(*, db: AsyncSession = Depends(deps.get_db), id_: int):
    cargo: models.CargoModel = await crud.cargo.get(db, id_)
    if not cargo:
        raise HTTPException(status_code=404, detail="Cargo not found")
    cargo = await crud.cargo.remove(db, cargo)
    return cargo


