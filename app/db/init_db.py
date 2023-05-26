import os
from sqlalchemy.ext.asyncio import AsyncSession
import csv
from app.core.config import get_settings
from app.db import base
from app import crud, schemas
from app.schemas.location import LocationSchema


# Loading file with zip codes
async def init_db(db: AsyncSession) -> None:
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
