import csv
import asyncio
import logging
from app.db.session import Session
from app import crud
from app.schemas.location import LocationSchema
from app.models.truck import TruckModel


async def repeater(db: Session, timeout: int = 3):
    while True:
        await asyncio.sleep(timeout * 60)
        logging.info("Refill Trucks")
        trucks: list[TruckModel] = await crud.truck.get_all_trucks(db)
        lst_id = await crud.location.get_random_locations_id(db, 20)
        for counter, truck in enumerate(trucks):
            await crud.truck.update(db, id_=truck.id, location=lst_id[counter])


# Init start data
async def init_db(db: Session) -> None:
    await fill_location(db)
    await fill_truck(db)
    asyncio.create_task(repeater(db, timeout=3))


async def fill_location(db: Session):
    f_name = "uszips.csv"
    is_exists = await crud.location.get_first(db)
    if not is_exists:
        data: list[LocationSchema] = []
        with open(f_name, "r") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                data.append(LocationSchema(
                    town=row["city"],
                    state=row["state_name"],
                    zip=int(row["zip"]),
                    lat=float(row["lat"]),
                    lng=float(row["lng"])
                ))

        await crud.location.create_init(db, obj_in=data)


async def fill_truck(db: Session):
    truck = await crud.truck.get(db, 1)
    if not truck:
        lst_id = await crud.location.get_random_locations_id(db, 20)
        await crud.truck.create_init(db, lst_id)
